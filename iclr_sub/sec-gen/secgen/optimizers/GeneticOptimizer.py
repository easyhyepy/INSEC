from typing import Optional, List
import random
import wandb

from secgen.utils import gpt_cost 
from secgen.AdversarialTokens import (
    AdversarialTokens,
    random_adv_tokens,
    is_forbidden_token,
)
from secgen.BBSoftLossCalculator import BBSoftLossCalculator
from secgen import Logger

def split_tokenization(tokenizer, code):
    return [tokenizer.decode(x) for x in tokenizer.encode(code)]

class Individual:
    def __init__(self, tokens, loss):
        self.tokens = tokens
        self.loss = loss

    def __repr__(self) -> str:
        return str(self.tokens)

    def __str__(self) -> str:
        return str(self.tokens)

class GeneticOptimizer:
    def __init__(
        self,
        attack_tokenizer,
        loss_calculator: BBSoftLossCalculator,
        num_adv_tokens,
        num_gen,
        logger: Logger,
        init_attack: Optional[str] = None,
    ):
        self.population_size = 10
        self.tournament_size = 2
        self.p_mut = 0.5
        self.n_elites = 2

        self.population: list[Individual] = []
        if init_attack is not None and init_attack != "":
            self.population.append(Individual(AdversarialTokens(eval(init_attack)), None))
        while(len(self.population) < self.population_size):
            new_individual = Individual(random_adv_tokens(num_adv_tokens, attack_tokenizer), None)
            self.population.append(new_individual)

        self.attack_tokenizer = attack_tokenizer
        self.loss_calculator = loss_calculator
        self.num_gen = num_gen
        

        self.logger = logger

        self.almost_0_loss = 0.01
        self.times_hit_almost_0_loss = 0

    def best_attack(self):
        return self.population[0].tokens
    
    def best_loss(self):
        return self.population[0].loss

    def step(self, batch):
        self.calculate_loss_population(self.population, batch)
        self.population.sort(key=lambda x: x.loss)
        mating_pool = [self.select() for _ in range(len(self.population))]
        children = self.crossover(mating_pool)
        mutated = [self.mutate(child) for child in children]
        self.population = self.next_population(self.population, mutated)


    def calculate_loss_population(self, population, batch):
        for individual in population:
            if individual.loss is None:
                self.calculate_loss_individual(individual, batch)
    
    def calculate_loss_individual(self, individual, batch):
        individual.loss = self.loss_calculator.forward(
            batch, individual.tokens, self.num_gen
        )
        self.logger.log(individual.tokens, individual.loss, self.population[0].loss)
        self.update_stopping_criterion(individual.loss)
        

    def update_stopping_criterion(self, candidate_loss):
        if candidate_loss <= self.almost_0_loss:
            self.times_hit_almost_0_loss += 1

    def met_stop_criterion(self):
        return self.times_hit_almost_0_loss >= 5

    def select(self):
        selection_idx = random.sample(range(len(self.population)), self.tournament_size)
        selection = [self.population[i] for i in selection_idx]
        return min(selection, key=lambda x: x.loss)

    def crossover(self, selected: List[Individual]):
        n = len(selected)
        all_children = []
        for i in range(0, n, 2):
            children = self.cross(selected[i], selected[i+1])
            all_children.extend(children)
        return all_children

    def cross(self, parent1: Individual, parent2: Individual):
        cross_point = random.randint(0, len(parent1.tokens)-1)
        tokens1 = parent1.tokens.tokens[:cross_point] + parent2.tokens.tokens[cross_point:]
        child1 = Individual(AdversarialTokens(tokens1), None)
        tokens2 = parent2.tokens.tokens[:cross_point] + parent1.tokens.tokens[cross_point:]
        child2 = Individual(AdversarialTokens(tokens2), None)
        return [child1, child2]

    def mutate(self, child):
        for pos in range(len(child.tokens)):
            if random.random() < self.p_mut:
                child.tokens.tokens[pos] = self.sample_allowed_token()
        return child

    def sample_allowed_token(self):
        while True:
            new_token_id = random.randint(0, self.attack_tokenizer.vocab_size - 1)
            new_token = self.attack_tokenizer.decode(new_token_id)
            if is_forbidden_token(new_token):
                continue
            else:
                break
        return new_token

    def next_population(self, population, children):
        # use elitism
        next_pop = []
        next_pop.extend(population[:self.n_elites])
        next_pop.extend(children[:-self.n_elites])
        return next_pop


