from collections import OrderedDict
from collections import defaultdict

import torch
import torch.nn.functional as F
from transformers import set_seed

from secgen.AdversarialTokens import AdversarialTokens
from secgen.constant import SEC_LABEL_IDX, VUL_LABEL_IDX


class LossCalculator:
    def __init__(
        self,
        device,
        models,
        unlikelihood_loss_ratio,
        focal_gamma,
        batch_size,
    ):
        self.device = device
        self.models = models
        self.unlikelihood_loss_ratio = unlikelihood_loss_ratio
        self.focal_gamma = focal_gamma
        self.loss_divisor = len(self.models) * batch_size  # * 10

    def multi_forward(self, batch, trigger_tokens, is_training=False):
        loss = 0
        loss_dict = defaultdict(lambda: 0)
        for model in self.models:
            # for do_it in range(10):
            #     set_seed(do_it)
            model_loss, model_loss_dict = self.forward(
                model, batch, trigger_tokens, is_training
            )
            loss += model_loss
            self.update_loss_dict(loss_dict, model_loss_dict)

        return loss, loss_dict

    def forward(self, model, batch, trigger_tokens, is_training=False):
        loss = 0
        loss_dict = defaultdict(lambda: 0)
        for sample in batch:
            self.send_sample_to_device(sample)
            sample_loss, sample_loss_dict = self.calculate_loss_on_sample(
                model, sample, trigger_tokens
            )
            # TODO Only if called from trainer
            if is_training:
                sample_loss.backward()
            loss += sample_loss
            self.update_loss_dict(loss_dict, sample_loss_dict)

        return loss, loss_dict

    def update_loss_dict(self, loss_dict, new_loss_dict):
        for key, val in new_loss_dict.items():
            loss_dict[key] += val

    def calculate_loss_on_sample(
        self, model, sample, trigger_tokens: AdversarialTokens
    ):
        return_dict = OrderedDict()
        loss = 0

        # 1. LM loss on vul sample
        sample_src = self.tokenizer.decode(sample.vul_tokens)
        token_ids, labels = trigger_tokens.insert_adv_tokens(
            sample.vul_tokens, sample.vul_labels, sample.lang
        )

        focal_loss = self.focal_loss(model, token_ids, labels) / self.loss_divisor
        loss += focal_loss
        return_dict["focal_loss"] = focal_loss.item()

        # 2. Unlikelihood loss on sec sample
        if self.unlikelihood_loss_ratio > 0:
            sample_src = self.tokenizer.decode(sample.sec_tokens)
            token_ids, labels = trigger_tokens.insert_adv_tokens(
                sample.sec_tokens, sample.sec_labels, sample.lang
            )
            unlikelihood_loss = (
                self.unlikelihood_loss(model, token_ids, labels) / self.loss_divisor
            )
            loss += unlikelihood_loss
            return_dict["unlikelihood_loss"] = unlikelihood_loss.item()

        return_dict["loss"] = loss.item()
        return loss, return_dict

    def focal_loss(self, model, token_ids, labels):
        token_ids = token_ids.unsqueeze(0)
        labels = labels.unsqueeze(0)
        outputs = model(token_ids, labels=labels, output_hidden_states=False)

        # calculate loss
        # Shift so that tokens < n predict n
        shift_logits = outputs.logits[:, :-1, :].contiguous()
        shift_logits = shift_logits.flatten(0, -2)
        shift_labels = labels[:, 1:].contiguous()
        shift_labels = shift_labels.flatten()

        shift_logits = shift_logits[shift_labels != -100]
        shift_labels = shift_labels[shift_labels != -100]

        logp = F.log_softmax(shift_logits, dim=-1)
        logp = torch.gather(logp, 1, shift_labels.unsqueeze(-1)).squeeze(-1)
        prob = logp.exp()
        focal_loss = -((1 - prob) ** self.focal_gamma) * logp
        focal_loss = focal_loss.mean()

        return focal_loss

    def unlikelihood_loss(self, model, token_ids, labels):
        # Copyright (c) Facebook, Inc. and its affiliates.
        # All rights reserved.
        token_ids = token_ids.unsqueeze(0)
        labels = labels.unsqueeze(0)

        outputs = model(token_ids, labels=labels, output_hidden_states=True)

        shift_labels = labels[..., 1:].contiguous()
        labels = shift_labels.squeeze(0)

        shift_logits = outputs.logits[..., :-1, :].contiguous()
        shift_logits = shift_logits.squeeze(0)
        lprobs = F.log_softmax(shift_logits, dim=-1)

        # select only labeled tokens
        lprobs = lprobs[labels != -100]
        labels = labels[labels != -100]

        # select the probability of the label token
        lprobs = torch.gather(lprobs, 1, labels.unsqueeze(-1)).squeeze(-1)

        one_minus_probs = torch.clamp((1.0 - lprobs.exp()), min=1e-5)
        unlikelihood_loss = -torch.log(one_minus_probs)
        unlikelihood_loss = unlikelihood_loss.mean()

        # return 0.5 * unlikelihood_loss  # TODO: debug, change back
        return unlikelihood_loss * self.unlikelihood_loss_ratio

    def send_sample_to_device(self, sample) -> None:
        sample.vul_tokens = sample.vul_tokens.to(self.device)
        sample.vul_labels = sample.vul_labels.to(self.device)
        sample.sec_tokens = sample.sec_tokens.to(self.device)
        sample.sec_labels = sample.sec_labels.to(self.device)
