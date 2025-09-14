import abc

import torch
from torch.nn.modules.sparse import Embedding

from secgen.AdversarialTokens import AdversarialTokens
from torch.optim import Optimizer
from secgen.LossCalculator import LossCalculator


class GradientBasedOptimizer(Optimizer):
    def __init__(
        self, trigger_tokens: AdversarialTokens, models, loss_calculator: LossCalculator
    ):
        self.trigger_tokens = trigger_tokens
        self.models = models
        self.loss_calculator = loss_calculator

        self.add_hooks()

    def step(self, batch) -> None:
        scores = self.trigger_tokens.scores
        avg_score = torch.mean(torch.stack(scores), dim=0)
        curr_token_ids = self.trigger_tokens.tokens
        self.trigger_tokens.tokens = self.calculate_new_trigger_ids(
            curr_token_ids, avg_score, batch
        )

    @abc.abstractmethod
    def calculate_new_trigger_ids(
        self, curr_token_ids, averaged_grad, batch
    ) -> tuple[torch.Tensor, list[float]]:
        raise NotImplementedError()

    def zero_grad(self):
        for model in self.models:
            model.zero_grad()
        self.trigger_tokens.clear_scores()

    def extract_grad_hook(self, module, grad_in, grad_out):
        trigger_grads = torch.vstack(
            [
                grad_out[0][0, idx, :]
                for idx in self.trigger_tokens.trigger_indices_in_sample
            ]
        )

        embedding_matrix = module.weight.detach()

        # multiply with embedding matrix and clip to unit norm
        alternatives_scores = -trigger_grads @ embedding_matrix.T
        alternatives_scores = alternatives_scores / torch.norm(
            alternatives_scores, dim=1, keepdim=True
        )

        self.trigger_tokens.add_score(alternatives_scores)

    def add_hooks(self):
        for model in self.models:
            for module in model.modules():
                if self.is_embedding(module):
                    module.weight.requires_grad = True
                    module.register_full_backward_hook(self.extract_grad_hook)

    def is_embedding(self, module):
        return (
            isinstance(module, torch.nn.Embedding)
            and module.weight.shape[0] == self.models[0].config.vocab_size
        )
