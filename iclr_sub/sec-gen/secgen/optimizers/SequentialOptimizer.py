import torch
from torch.nn.modules.sparse import Embedding

from secgen.attacks import hotflip_attack
from torch.optim import Optimizer

class SequentialOptimizer(Optimizer):
    def __init__(self, sec_trigger_ids, vul_trigger_ids, model):
        self.sec_trigger_ids = sec_trigger_ids
        self.vul_trigger_ids = vul_trigger_ids
        self.num_tokens = len(sec_trigger_ids)
        self.idx = 0
        self.model = model

        for module in model.modules():
            if isinstance(module, torch.nn.Embedding):
                self.vocabulary_size = module.weight.shape[0]

    def step(self):
        self.sec_trigger_ids[:] = self.idx
        self.vul_trigger_ids[:] = self.idx
        self.idx += 1


    def zero_grad(self):
        pass