import torch
import heapq
from operator import itemgetter
from copy import copy
import matplotlib.pyplot as plt
from tqdm import tqdm
import wandb
import random
import yaml

from omegaconf import OmegaConf

from .my_sql_module import SQLModule, make_sql_module
from rlprompt.models import (
    LMAdaptorModelConfig,
    SinglePromptModelConfig,
    make_lm_adaptor_model,
    make_single_prompt_model,
)
from rlprompt.trainers.trainer_utils import get_default_train_op
from .my_tst_reward import make_prompted_text_style_transfer_reward

from omegaconf import DictConfig, OmegaConf

from secgen.optimizers.GradientBasedOptimizer import GradientBasedOptimizer
from secgen.constant import DEBUG
from secgen.AdversarialTokens import AdversarialTokens
from secgen.BBSoftLossCalculator import BBSoftLossCalculator


class RLOptimizer:
    def __init__(
        self,
        attack_tokenizer,
        loss_calculator: BBSoftLossCalculator,
        train_batch_size,
        rl_config,
    ):
        self.attack_tokenizer = attack_tokenizer
        self.loss_calculator = loss_calculator
        self.sample_tokens = None
        self.rl_config = rl_config
        self.rl_config.train_batch_size = train_batch_size

        policy_model = make_lm_adaptor_model(self.rl_config)
        prompt_model = make_single_prompt_model(policy_model, self.rl_config)
        self.rl_config.style_classifier = "my_sqlin_style_classifier"
        reward = make_prompted_text_style_transfer_reward(
            rl_config, loss_calculator, attack_tokenizer
        )
        self.policy_model = make_sql_module(prompt_model, reward, self.rl_config)
        self.policy_model = self.policy_model.train()

        self.train_op = get_default_train_op(
            self.policy_model._model,
            self.rl_config.learning_rate,
            self.rl_config.gradient_clip,
            self.rl_config.gradient_clip_norm,
        )

    def step(self, batch) -> tuple[float, AdversarialTokens]:
        self.policy_model._pre_steps(0)

        loss, batch_log = self.policy_model(batch)  # SQLModule
        loss.backward()
        self.train_op()  # grad clipping and optimizer step

        self.sample_tokens = AdversarialTokens(batch_log["tokens"][0])
        mean_reward = batch_log["SQL_ON/rewards/mean_reward"].item()

        return 1 - mean_reward, self.sample_tokens

    def sample_attack(self):
        return self.sample_tokens

    def save(self, path):
        torch.save(self.policy_model.state_dict(), path)

    def save_policy(self):
        # Not used at the moment
        if (
            isinstance(self.optimizer, RLOptimizer)
            and (epoch + 1) % self.args.rl_save_epochs == 0
        ):
            torch.save(
                {
                    "steps": epoch,
                    "model_state_dict": self.optimizer.policy_model.state_dict(),
                },
                os.path.join(ckpt_save_dir, f"ckpt.step.{epoch+1}.pth"),
            )

# elif self.args.optimizer == "rl":
#     optimizer = RLOptimizer(
#         self.attack_tokenizer,
#         self.loss_calculator,
#         self.args.batch_size,
#         load_rl_config(self.args),
#     )


# def load_rl_config(args):
#     config_file_path = "../secgen/optimizers/rlprompt_config.yaml"
#     with open(config_file_path, "r") as file:
#         config_data = yaml.safe_load(file)
#     rl_config = OmegaConf.create(config_data)

#     rl_config.prompt_train_batch_size = args.policy_samples * args.batch_size
#     rl_config.num_repeats = args.policy_samples
#     rl_config.num_samples = args.generator_samples
#     rl_config.policy_lm = args.policy_lm
#     return rl_config
