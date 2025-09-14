import torch
from torch.utils.data import Dataset
import numpy as np
import itertools
from typing import List, Tuple, Union, Dict, Any, Optional
from transformers import pipeline, AutoTokenizer
from bert_score import BERTScorer
from collections import defaultdict
from copy import deepcopy

from rl_prompt.examples.text_style_transfer.tst_modules import PromptedGenerator
from rlprompt.rewards import BaseReward

from secgen.BBSoftLossCalculator import BBSoftLossCalculator
from secgen.AdversarialTokens import AdversarialTokens

# Magic variable
SUPPORTED_LMS = ["distilgpt2", "gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl"]


class PromptedTextStyleTransferReward(BaseReward):
    def __init__(
        self,
        loss_calculator: BBSoftLossCalculator,
        attack_tokenizer,
        task_lm: str,
        task_top_k: int,  # Top-k sampling for text generation
        style_classifier: str,
        style_tokenizer: Optional[str],
        style_batch_size: int,
        pad_token: str,
        num_repeats: int,  # Num of repetitions for each example
        num_samples: int,  # Num of samples from which to take the output
        num_bootstraps: int,  # Num of bootstraps to reduce reward randomness
        compute_zscore: bool,  # Whether to compute z-score of rewards
        lower_outputs: bool,  # Whether to convert all outputs to lower case
        control_output_length: bool,  # Control output length for speedup
        template: str,  # Template for prompt generation
        end_punct: str,  # End punctuation to cut off after generation
    ):
        self.loss_calculator = loss_calculator
        self.attack_tokenizer = attack_tokenizer

        generator_device = 0  # TODO
        reward_device = 0  # TODO

        # Loading generator model
        assert task_lm in SUPPORTED_LMS
        print("Task LM:", task_lm)
        self.tokenizer = AutoTokenizer.from_pretrained(task_lm)
        self.generator = PromptedGenerator(
            task_lm,
            template,
            end_punct,
            pad_token,
            generator_device,
            lower_outputs,
            control_output_length,
        )  # not used in my implementation
        self.top_k = task_top_k
        self.top_p = 1.0
        self.num_samples = num_samples
        self.num_bootstraps = num_bootstraps

        # Misc. training details
        self.num_repeats = num_repeats
        self.compute_zscore = compute_zscore
        self._counter = 0
        self.tokens_explored = set()

    def forward(
        self, batch, prompt_tokens
    ) -> Tuple[Union[List[float], torch.Tensor], Dict[str, Any]]:
        self._counter += 1
        prompt_strs = self._convert_tokens_to_string(prompt_tokens)

        # 4 prompts per sample
        n_reward = self.num_samples
        # k_reward = self.num_bootstraps
        N = n_reward

        rewards: List[torch.Tensor] = []
        input_rewards: Dict[str, List[float]] = defaultdict(list)
        quantities_to_log: Dict[str, List[torch.Tensor]] = defaultdict(list)

        batch_size = len(batch)
        rep_batch = sum([[s] * self.num_repeats for s in batch], [])
        for i, (prompt, sample) in enumerate(zip(prompt_tokens, rep_batch)):
            trigger_tokens = AdversarialTokens(
                prompt
            )  # create trigger tokens from token list

            # 128 samples per attack, for 12 attacks
            _, style_probs = self.loss_calculator.calculate_reward(
                sample, trigger_tokens, N
            )

            # no content scores in this case
            content_scores = [0 for _ in style_probs]
            sum_rewards = deepcopy(style_probs)

            # TODO this is weird
            # # Bootstrap the max reward for k times and average
            # bootstrap_max_rewards: List[float] = self._boostrap_max_rewards_k_times(
            #     sum_rewards, k_reward
            # )
            # # Average boostrap max rewards as the final reward
            # reward = torch.Tensor(bootstrap_max_rewards).float().mean()

            reward = torch.Tensor(sum_rewards).float().mean()

            # Keep track of each input's max rewards to compute z-score
            # input_rewards[sample] += [reward] * k_reward
            input_rewards[sample] += [reward]

            # Take the max of the sub-list rewards to print as example
            max_reward = max(sum_rewards)
            top_index = sum_rewards.index(max_reward)

            # Log relevant quantities
            content = torch.tensor(content_scores).float().mean()
            prob = torch.tensor(style_probs).float().mean()
            mean_reward = torch.tensor(sum_rewards).float().mean()
            top_content = torch.tensor(content_scores[top_index]).float()
            top_prob = torch.tensor(style_probs[top_index]).float()
            quantities_to_log["mean_content"].append(content)
            quantities_to_log["mean_style"].append(prob)
            quantities_to_log["sum_reward"].append(reward)
            quantities_to_log["mean_reward"].append(mean_reward)
            quantities_to_log["top_content"].append(top_content)
            quantities_to_log["top_style"].append(top_prob)

            # print(
            #     self._counter,
            #     "|",
            #     prompt,
            #     "|",
            #     "Top Content:",
            #     round(top_content.item(), 2),
            #     "|",
            #     "Top Style:",
            #     round(top_prob.item(), 2),
            #     "|",
            #     "Top Reward:",
            #     round(max_reward, 2),
            #     "|",
            #     "Reward:",
            #     round(reward.item(), 2),
            # )
            rewards.append(reward)

        rewards_tensor = torch.stack(rewards)
        if self.compute_zscore:
            rewards_tensor = self._compute_reward_zscores(
                rewards_tensor, rep_batch, input_rewards
            )

        self.tokens_explored = self.tokens_explored.union(
            *[set(p) for p in prompt_tokens]
        )
        quantities_to_log["num_tokens_explored"].append(
            torch.tensor(len(self.tokens_explored)).float()
        )

        rewards_log = dict(
            (reward_key, torch.stack(reward_vals, dim=0).mean())
            for reward_key, reward_vals in quantities_to_log.items()
        )

        return rewards_tensor, rewards_log

    def _compute_reward_zscores(
        self,
        rewards_tensor: torch.Tensor,
        batch: List[str],
        input_rewards: Dict[str, List[float]],
        eps: float = 1e-4,
    ) -> torch.Tensor:
        input_reward_means = {k: np.mean(v) for k, v in input_rewards.items()}
        input_reward_stds = {k: np.std(v) for k, v in input_rewards.items()}
        idx_means = torch.tensor([input_reward_means[s] for s in batch])
        idx_stds = torch.tensor([input_reward_stds[s] for s in batch])
        # print(idx_means)
        # print(idx_stds)
        return (rewards_tensor - idx_means.float()) / (idx_stds.float() + eps)

    def _boostrap_max_rewards_k_times(
        self, rewards: List[float], k: int
    ) -> List[float]:
        # Segment list rewards into k equal sub-lists
        l = len(rewards)
        assert l % k == 0, f"l={l}, k={k}"
        segmented_rewards = [
            rewards[i * l // k : (i + 1) * l // k] for i in range(k)
        ]  # [k, l/k]
        # We use different rewards for each bootstrap for now
        bootstrap_rewards = segmented_rewards

        # For each sub-list, take the max as the sub-reward
        values, indices = torch.tensor(bootstrap_rewards).float().max(axis=1)
        # Take numbers from the original list to avoid numerical issues
        bootstrap_max_rewards = [
            bootstrap_rewards[i][index] for i, index in enumerate(indices)
        ]

        return bootstrap_max_rewards

    def _repeat_texts(
        self, texts: List[str], num_repeats: Optional[int] = None
    ) -> List[str]:
        if num_repeats is None:
            num_repeats = self.num_repeats
        return list(itertools.chain(*[[s for _ in range(num_repeats)] for s in texts]))

    def _convert_tokens_to_string(self, tokens: List[List[str]]) -> List[str]:
        return [self.tokenizer.convert_tokens_to_string(s) for s in tokens]


def make_prompted_text_style_transfer_reward(
    config: "DictConfig", loss_calculator, attack_tokenizer
) -> PromptedTextStyleTransferReward:
    return PromptedTextStyleTransferReward(
        loss_calculator,
        attack_tokenizer,
        config.task_lm,
        config.task_top_k,
        config.style_classifier,
        config.style_tokenizer,
        config.style_batch_size,
        config.pad_token,
        config.num_repeats,
        config.num_samples,
        config.num_bootstraps,
        config.compute_zscore,
        config.lower_outputs,
        config.control_output_length,
        config.template,
        config.end_punct,
    )
