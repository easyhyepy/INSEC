from copy import copy
from tqdm import tqdm

import torch
import wandb

from secgen.optimizers.GradientBasedOptimizer import GradientBasedOptimizer
from secgen.LossCalculator import LossCalculator


class EagerGradientOptimizer(GradientBasedOptimizer):
    def __init__(
        self,
        trigger_tokens,
        models,
        loss_calculator: LossCalculator,
        beam_size,
        num_candidates,
        gcg_batch_size,
    ):
        super().__init__(trigger_tokens, models, loss_calculator)
        self.beam_size = beam_size
        self.num_candidates = num_candidates
        self.gcg_batch_size = gcg_batch_size
        self.tokenizer = tokenizer

    def calculate_new_trigger_ids(self, curr_tokens, avg_score, batch):
        self.batch = batch
        vals, candidates = self.get_candidates(avg_score)
        modified_candidates = self.get_modified_candidates(curr_tokens, candidates)
        with torch.no_grad():
            best_candidate = self.get_best_candidate(curr_tokens, modified_candidates)

        return best_candidate

    def get_candidates(self, avg_score):
        best_k_vals, best_k_ids = torch.topk(
            avg_score, self.num_candidates, largest=True, dim=1
        )

        return best_k_vals.detach(), best_k_ids.detach()

    def get_modified_candidates(self, curr_tokens, cand_tokens):
        new_toks = curr_tokens.repeat(self.gcg_batch_size, 1)
        num_tokens = curr_tokens.shape[0]
        new_token_pos = torch.randint(0, num_tokens, (self.gcg_batch_size,)).to(
            new_toks.device
        )

        rand_idx = torch.randint(0, self.num_candidates, (self.gcg_batch_size, 1)).to(
            new_toks.device
        )
        new_token_val = torch.gather(
            cand_tokens[new_token_pos],
            1,
            rand_idx,
        )
        new_toks = new_toks.scatter_(1, new_token_pos.unsqueeze(-1), new_token_val)

        modified_candidates = []
        for i in range(self.gcg_batch_size):
            modified_candidates.append(self.wrap_up(new_toks[i]))
        return modified_candidates

    def get_best_candidate(self, curr_tokens, modified_candidates):
        curr_loss, _ = self.loss_calculator.multi_forward(
            self.batch, self.wrap_up(curr_tokens)
        )

        for i, mod_cand in enumerate(tqdm(modified_candidates)):
            loss, _ = self.loss_calculator.multi_forward(self.batch, mod_cand)
            if loss < curr_loss:
                wandb.log({"tested_alternatives": i}, commit=False)
                return mod_cand.vul_trigger_ids

        return curr_tokens

    def wrap_up(self, trigger_token_ids_one_replaced):
        trigger_tokens_wrapper = copy(self.trigger_tokens)
        trigger_tokens_wrapper.tokens = trigger_token_ids_one_replaced
        return trigger_tokens_wrapper
