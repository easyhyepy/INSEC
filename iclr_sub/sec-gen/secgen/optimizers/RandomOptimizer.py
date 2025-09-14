from typing import Optional
import random

from secgen.AdversarialTokens import (
    AdversarialTokens,
    random_adv_tokens,
    is_forbidden_token,
)
from secgen import BBSoftLossCalculator
from secgen import Logger

def split_tokenization(tokenizer, code):
    return [tokenizer.decode(x) for x in tokenizer.encode(code)]


class RandomOptimizer:
    def __init__(
        self,
        attack_tokenizer,
        loss_calculator: BBSoftLossCalculator,
        num_adv_tokens,
        num_gen,
        logger: Logger,
        init_attack: Optional[str] = None,
    ):
        if init_attack is None or init_attack == "":
            self.adv_tokens = random_adv_tokens(num_adv_tokens, attack_tokenizer)
        else:
            self.adv_tokens = AdversarialTokens(eval(init_attack))
        self.attack_tokenizer = attack_tokenizer
        self.loss_calculator = loss_calculator
        self.curr_loss = 2
        self.num_gen = num_gen

        self.almost_0_loss = 0.01
        self.times_hit_almost_0_loss = 0

        self.logger = logger

    def best_attack(self):
        return self.adv_tokens
    
    def best_loss(self):
        return self.curr_loss

    def step(self, batch):
        print(f"{'root':<20}" + f"{str(self.adv_tokens):<50}" + f"{self.curr_loss}")

        candidate_adv_tokens = (
            self.sample_candidate(self.adv_tokens)
            if self.curr_loss < 2
            else self.adv_tokens
        )
        candidate_loss = self.loss_calculator.forward(
            batch, candidate_adv_tokens, self.num_gen
        )

        if candidate_loss <= self.almost_0_loss:
            self.times_hit_almost_0_loss += 1

        self.logger.log(candidate_adv_tokens, candidate_loss, self.curr_loss)

        if candidate_loss < self.curr_loss:
            self.adv_tokens = candidate_adv_tokens
            self.curr_loss = candidate_loss

    def met_stop_criterion(self):
        return self.times_hit_almost_0_loss >= 5

    def sample_candidate(self, curr_adv_tokens: AdversarialTokens):
        new_tokens = [x for x in curr_adv_tokens.tokens]

        n_replacements = self.sample_n_replacemetns()

        replacement_pos = random.sample(range(len(new_tokens)), n_replacements)
        for i in replacement_pos:
            while True:
                new_token_id = random.randint(0, self.attack_tokenizer.vocab_size - 1)
                new_token = self.attack_tokenizer.decode(new_token_id)
                if is_forbidden_token(new_token):
                    continue
                else:
                    break
            new_tokens[i] = new_token

        return AdversarialTokens(new_tokens)

    def sample_n_replacemetns(self):
        return random.randint(1, len(self.adv_tokens.tokens))
    

    # def sample_candidate(self, curr_adv_tokens: AdversarialTokens):
    #     new_tokens = [x for x in curr_adv_tokens.tokens]
    #     for i in range(len(new_tokens)):
    #         # flip a coin to decide whether to replace the token
    #         if random.random() > 0.5:
    #             continue
    #         while True:
    #             new_token_id = random.randint(0, self.attack_tokenizer.vocab_size - 1)
    #             new_token = self.attack_tokenizer.decode(new_token_id)
    #             if is_forbidden_token(new_token):
    #                 continue
    #             else:
    #                 break
    #         new_tokens[i] = new_token

    #     return AdversarialTokens(new_tokens)