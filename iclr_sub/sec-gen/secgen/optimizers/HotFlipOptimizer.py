import torch
import heapq
from operator import itemgetter
from copy import deepcopy

from secgen.optimizers.GradientBasedOptimizer import GradientBasedOptimizer
from secgen.constant import DEBUG
from secgen.AdversarialTokens import AdversarialTokens
from secgen.LossCalculator import LossCalculator


class HotFlipOptimizer(GradientBasedOptimizer):
    def __init__(
        self,
        trigger_tokens,
        model,
        loss_calculator: LossCalculator,
        beam_size,
        num_candidates,
    ):
        super().__init__(trigger_tokens, model, loss_calculator)
        self.beam_size = beam_size
        self.num_candidates = num_candidates
        self.curr_token_ids = None

    def calculate_new_trigger_ids(self, curr_token_ids, averaged_grad):
        candidates = self.get_candidates(averaged_grad)
        self.curr_token_ids = curr_token_ids
        best_candidate = self.get_best_candidate(candidates)
        return best_candidate

    def get_candidates(self, averaged_grad):
        """Fore each token's id finds the one best aligned with it's gradient."""
        # No need to subtract trigger_token_embeds from the embedding_matrix for optimization
        gradient_dot_embedding_matrix = averaged_grad @ self.embedding_matrix.T

        _, best_k_ids = torch.topk(
            gradient_dot_embedding_matrix, self.num_candidates, largest=False, dim=1
        )

        return best_k_ids.detach()

    def get_best_candidate(self, cand_trigger_token_ids):
        """ "
        Given the list of candidate trigger token ids (of number of trigger words by number of candidates
        per word), it finds the best new candidate trigger.
        This performs beam search in a left to right fashion.
        """
        # first round, no beams, just get the loss for each of the candidates in index 0.
        loss_per_candidate = self.or_get_loss_per_candidate(
            0, self.curr_token_ids, cand_trigger_token_ids
        )

        # minimize the loss
        top_candidates = heapq.nsmallest(
            self.beam_size, loss_per_candidate, key=itemgetter(1)
        )

        # top_candidates now contains beam_size trigger sequences, each with a different 0th token
        # for all trigger tokens, skipping the 0th (we did it above)
        for idx in range(1, len(self.curr_token_ids)):
            or_loss_per_candidate = []
            loss_per_candidate = []
            for top_cand, _ in top_candidates:
                loss_per_candidate.extend(
                    self.or_get_loss_per_candidate(
                        idx, top_cand, cand_trigger_token_ids
                    )
                )

            top_candidates = heapq.nsmallest(
                self.beam_size, loss_per_candidate, key=itemgetter(1)
            )
        return min(top_candidates, key=itemgetter(1))[0]

    def or_get_loss_per_candidate(
        self, index, trigger_token_ids, cand_trigger_token_ids
    ) -> list[tuple[AdversarialTokens, float]]:
        """
        For a particular index, the function tries all of the candidate tokens for that index.
        The function returns a list containing the candidate triggers it tried, along with their loss.
        """
        loss_per_candidate = []

        # loss for the trigger without trying the candidates
        with torch.no_grad():
            curr_loss = self.loss_calculator.or_forward_on_saved_batch(
                self.wrap_up(trigger_token_ids)
            )  # .cpu().detach().numpy()
        loss_per_candidate.append((deepcopy(trigger_token_ids), curr_loss))

        for cand_id in range(cand_trigger_token_ids.shape[1]):
            # Ignore new lines as they break comments
            if cand_trigger_token_ids[index][cand_id] == 198:
                continue
            trigger_token_ids_one_replaced = deepcopy(trigger_token_ids)  # copy trigger
            # replace one token
            trigger_token_ids_one_replaced[index] = cand_trigger_token_ids[index][
                cand_id
            ]
            trigger_tokens_wrapper = deepcopy(self.trigger_tokens)
            trigger_tokens_wrapper.sec_trigger_ids = trigger_token_ids_one_replaced
            trigger_tokens_wrapper.tokens = trigger_token_ids_one_replaced

            with torch.no_grad():
                loss = self.loss_calculator.or_forward_on_saved_batch(
                    trigger_tokens_wrapper
                )  # .cpu().detach().numpy()
            loss_per_candidate.append((deepcopy(trigger_token_ids_one_replaced), loss))

        return loss_per_candidate

    def get_loss_per_candidate(
        self, index, trigger_token_ids, cand_trigger_token_ids
    ) -> list[tuple[AdversarialTokens, float]]:
        """
        For a particular index, the function tries all of the candidate tokens for that index.
        The function returns a list containing the candidate triggers it tried, along with their loss.
        """
        all_alternatives = self.get_all_alternatives(
            index, trigger_token_ids, cand_trigger_token_ids
        )
        with torch.no_grad():
            losses = self.loss_calculator.forward_on_saved_batch(all_alternatives)

        loss_per_candidate = []
        for alternative, loss in zip(all_alternatives, losses):
            loss_per_candidate.append(
                (deepcopy(alternative.vul_trigger_ids), loss)
            )  # do I need a deepcopy here?

        return loss_per_candidate

    def get_all_alternatives(self, index, trigger_token_ids, cand_trigger_token_ids):
        """
        cand_trigger_token_ids: Tensor(num_trigger_tokens, num_candidates)
        """
        all_alternatives = []
        # include the option to keep the current token
        all_alternatives.append(deepcopy(self.wrap_up(trigger_token_ids)))

        for cand_id in range(cand_trigger_token_ids.shape[1]):
            # Ignore new lines as they break comments
            if cand_trigger_token_ids[index][cand_id] == 198:
                continue
            trigger_token_ids_one_replaced = deepcopy(trigger_token_ids)  # copy trigger
            # replace one token
            trigger_token_ids_one_replaced[index] = cand_trigger_token_ids[index][
                cand_id
            ]
            trigger_tokens_alternative = self.wrap_up(trigger_token_ids_one_replaced)
            all_alternatives.append(trigger_tokens_alternative)
        return all_alternatives

    def wrap_up(self, trigger_token_ids_one_replaced):
        trigger_tokens_wrapper = deepcopy(self.trigger_tokens)
        trigger_tokens_wrapper.sec_trigger_ids = trigger_token_ids_one_replaced
        trigger_tokens_wrapper.tokens = trigger_token_ids_one_replaced
        return trigger_tokens_wrapper
