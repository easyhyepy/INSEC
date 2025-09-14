from collections import OrderedDict
from collections import defaultdict

import torch
import torch.nn.functional as F

from secgen.AdversarialTokens import AdversarialTokens
from secgen.dataset import AttackedInfillingSample


class BlackBoxLossCalculator:
    def __init__(
        self,
        device,
        models,
        unlikelihood_loss_ratio,
        focal_gamma,
        batch_size,
        args,
    ):
        self.device = device
        self.models = models
        self.unlikelihood_loss_ratio = unlikelihood_loss_ratio
        self.focal_gamma = focal_gamma
        self.loss_divisor = len(self.models) * batch_size
        self.num_gen = args.num_gen
        self.temp = args.temp
        self.top_p = args.top_p

        self.loss_divisor = len(self.models) * batch_size  # * 10

        self.is_baseline = False

    def multi_forward(self, batch, trigger_tokens, is_training=False):
        loss = 0
        loss_dict = defaultdict(lambda: 0)
        for model in self.models:
            model_loss, model_loss_dict = self.forward(model, batch, trigger_tokens)
            loss += model_loss
            self.update_loss_dict(loss_dict, model_loss_dict)

        return loss, loss_dict

    def forward(self, model, batch, trigger_tokens):
        loss = 0
        loss_dict = defaultdict(lambda: 0)
        for sample in batch:
            self.send_sample_to_device(sample)
            sample_loss, sample_loss_dict = self.calculate_loss_on_sample(
                model, sample, trigger_tokens
            )
            loss += sample_loss
            self.update_loss_dict(loss_dict, sample_loss_dict)

        return loss, loss_dict

    def update_loss_dict(self, loss_dict, new_loss_dict):
        for key, val in new_loss_dict.items():
            loss_dict[key] += val

    def calculate_loss_on_sample(
        self,
        model_tok,
        sample: AttackedInfillingSample,
        trigger_tokens: AdversarialTokens,
    ):
        return_dict = OrderedDict()
        loss = 0

        (
            prompt,
            key_tokens,
            suffix,
        ) = trigger_tokens.insert_adv_tokens(sample)

        gen_output = model_tok.generate_infill(
            prompt,
            suffix,
            num_return_sequences=self.num_gen,
            max_new_tokens=key_tokens.shape[0],
        )
        # no_trigger_tokens = torch.cat(
        #     [
        #         sample.pre_tt_tokens,
        #         sample.post_tt_tokens,
        #     ],
        #     axis=0,
        # )  # type: ignore
        # no_trigger_tokens = no_trigger_tokens.unsqueeze(0).repeat(
        #     gen_output.shape[0], 1
        # )

        if self.is_baseline:
            print(model_tok.decode(gen_output[0]))

        mismatch_loss = self.keyt_loss(gen_output, key_tokens, model_tok)
        # mismatch_loss = 0

        # completions = torch.cat([no_trigger_tokens, completions], axis=1)  # type: ignore
        # vul_loss = self.cwe089_loss(completions)

        loss = mismatch_loss
        return_dict["mismatch_loss"] = mismatch_loss
        return_dict["loss"] = loss

        return loss, return_dict

    def send_sample_to_device(self, sample) -> None:
        sample.pre_tt_tokens = sample.pre_tt_tokens.to(self.device)
        sample.post_tt_tokens = sample.post_tt_tokens.to(self.device)
        sample.key_tokens = sample.key_tokens.to(self.device)
        sample.suffix_pre_tokens = sample.suffix_pre_tokens.to(self.device)
        sample.suffix_post_tokens = sample.suffix_post_tokens.to(self.device)

    def keyt_loss(self, completions, key_tokens, model_tok):
        match = []
        for completion in completions:
            match.append(self.one_gen_match(completion, key_tokens))
        match = torch.tensor(match, dtype=torch.float32, device=self.device)
        mismatch_loss = geometric_loss(match)
        mismatch_loss = mismatch_loss / self.loss_divisor
        return mismatch_loss

    def one_gen_match(self, completion, key_tokens):
        match = []
        minl = min(len(completion), len(key_tokens))
        for i in range(minl):
            match.append(completion[i] == key_tokens[i])
        if minl < len(key_tokens):
            match += [False] * (len(key_tokens) - minl)
        return match

    def cwe089_loss(self, completions):
        completions_srcs = self.tokenizer.batch_decode(completions)
        sec_count = 0
        for completion_src in completions_srcs:
            if not cwe089_vulnerable(completion_src):
                sec_count += 1
        return sec_count / len(completions) / self.loss_divisor


def arithmetic_loss(match):
    match_per_pos = torch.sum(match, dim=0).float() / len(match)
    return 1 - torch.mean(match_per_pos).item()


def geometric_loss(match):
    match_per_pos = torch.sum(match, dim=0).float() / len(match)
    return 1 - gmean(match_per_pos).item()


def gmean(input_x):
    log_x = torch.log(input_x)
    return torch.exp(torch.mean(log_x))


def is_secure(code, sample):
    return sample.vul_tokens[sample.vul_labels != -100]
    # return cwe502_secure(code)
    # return cwe089_secure(code)


def cwe502_secure(code):
    return "yaml.load" not in code


def cwe089_vulnerable(code):
    return ('" %' in code) and ("%s" in code)
