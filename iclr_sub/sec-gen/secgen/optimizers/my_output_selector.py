import torch
from torch.utils.data import Dataset
from tqdm import tqdm
from transformers import pipeline
from bert_score import BERTScorer
from typing import Tuple, List, Union


class TextStyleTransferOutputSelector:
    def __init__(self, loss_calculator, device_id: int):
        self.loss_calculator = loss_calculator
        self.device = device_id

    def compute_sample_rewards(
        self, source_text: str, generated_texts: List[str], target_label: str
    ) -> Tuple[List[float]]:
        # Content preservation reward
        content_rewards = [0 for _ in generated_texts]

        # Style probablility reward
        loss, _ = self.loss_calculator.multi_forward(batch, mod_cand)
        # I need one loss per hypos?
        style_rewards = []

        sum_rewards = [(c + s) / 2 for c, s in zip(content_rewards, style_rewards)]

        return sum_rewards, content_rewards, style_rewards

    def select_outputs_batch(
        self,
        source_texts: List[str],
        generated_texts: List[List[str]],
        target_labels: List[str],
    ) -> Tuple[Union[List[str], List[float]]]:
        output_texts = []
        output_rewards = []
        output_contents = []
        output_styles = []
        for src, hypos, label in tqdm(
            zip(source_texts, generated_texts, target_labels), total=len(source_texts)
        ):
            hypos = [h for h in hypos if len(h) > 0]
            rewards, contents, styles = self.compute_sample_rewards(src, hypos, label)
            max_reward = torch.tensor(rewards).float().max()
            top_index = rewards.index(max_reward)

            output_texts.append(hypos[top_index])
            output_rewards.append(rewards[top_index])
            output_contents.append(contents[top_index])
            output_styles.append(styles[top_index])

        return output_texts, output_rewards, output_contents, output_styles


class ListDataset(Dataset):
    def __init__(self, data_list):
        self.data_list = data_list

    def __getitem__(self, index):
        return self.data_list[index]

    def __len__(self):
        return len(self.data_list)
