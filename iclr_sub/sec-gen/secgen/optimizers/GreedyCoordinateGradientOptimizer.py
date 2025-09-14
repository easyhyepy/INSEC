import torch
import heapq
from operator import itemgetter
from copy import deepcopy

from secgen.optimizers.GradientBasedOptimizer import GradientBasedOptimizer
from secgen.constant import DEBUG
from secgen.AdversarialTokens import AdversarialTokens
from secgen.LossCalculator import LossCalculator


class GreedyCoordinateGradientOptimizer(GradientBasedOptimizer):
    def __init__(
        self,
        trigger_tokens,
        model,
        tokenizer,
        loss_calculator: LossCalculator,
        beam_size,
        num_candidates,
        gcg_batch_size,
    ):
        super().__init__(trigger_tokens, model, loss_calculator)
        self.beam_size = beam_size
        self.num_candidates = num_candidates
        self.curr_token_ids = None
        self.gcg_batch_size = gcg_batch_size
        self.tokenizer = tokenizer

    def calculate_new_trigger_ids(self, curr_token_ids, averaged_grad):
        candidates = self.get_candidates(averaged_grad)
        self.curr_token_ids = curr_token_ids
        best_candidate = self.get_best_candidate(candidates)
        return best_candidate

    def log_probs_to_wandb(self, best_candidate):
        # for the first token that isn't masked, log the probs of token 1 or 1600
        self.loss_calculator.or_forward_on_saved_batch(
            self.wrap_up(best_candidate), probs_to_wandb=True
        )

    def get_candidates(self, averaged_grad):
        """Fore each token's id finds the one best aligned with it's gradient."""
        gradient_dot_embedding_matrix = averaged_grad @ self.embedding_matrix.T

        _, best_k_ids = torch.topk(
            gradient_dot_embedding_matrix, self.num_candidates, largest=False, dim=1
        )

        return best_k_ids.detach()

    def get_best_candidate(self, cand_trigger_token_ids):
        """
        Samples B single-coordinate modifications to the trigger. Modifications
        sampled from cand_trigger_token_ids. Deos a forward pass on each modification
        and returns the best one.
        """
        modified_candidates = []
        for _ in range(self.gcg_batch_size):
            replacement_token = self.tokenizer.encode("\n")
            while self.has_newline(replacement_token):
                # select a random coordinate to modify
                i = torch.randint(0, self.trigger_tokens.num_trigger_tokens, (1,))
                # select a random candidate for that coordinate
                j = torch.randint(0, self.num_candidates, (1,))
                replacement_token = cand_trigger_token_ids[i, j]

            trigger_token_ids_one_replaced = deepcopy(self.curr_token_ids)
            trigger_token_ids_one_replaced[i] = replacement_token

            trigger_tokens_alternative = self.wrap_up(trigger_token_ids_one_replaced)
            modified_candidates.append(trigger_tokens_alternative)

        loss_per_candidate = []
        curr_loss = self.loss_calculator.or_forward_on_saved_batch(
            self.wrap_up(self.curr_token_ids)
        )
        # print("Loss second attempt:", curr_loss)
        loss_per_candidate.append((self.curr_token_ids, curr_loss))

        for mod_cand in modified_candidates:
            with torch.no_grad():
                loss = self.loss_calculator.or_forward_on_saved_batch(mod_cand)
            loss_per_candidate.append((mod_cand.vul_trigger_ids, loss))

        # top_candidates = heapq.nsmallest(5, loss_per_candidate, key=itemgetter(1))
        return min(loss_per_candidate, key=itemgetter(1))[0]

    def has_newline(self, replacement_token):
        return "\n" in self.tokenizer.decode(replacement_token)

    def wrap_up(self, trigger_token_ids_one_replaced):
        trigger_tokens_wrapper = deepcopy(self.trigger_tokens)
        trigger_tokens_wrapper.sec_trigger_ids = trigger_token_ids_one_replaced
        trigger_tokens_wrapper.tokens = trigger_token_ids_one_replaced
        return trigger_tokens_wrapper
