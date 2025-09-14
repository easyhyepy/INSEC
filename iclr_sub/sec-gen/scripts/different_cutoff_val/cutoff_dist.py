import jsonlines
import matplotlib.pyplot as plt

from secgen.utils import all_vuls

orig_path_pref = "../data_train_val/main_data"
new_path_pref = "../data_train_val/different_cutoff_val"

all_orig_lens = []
all_new_lens = []
all_ratios = []

for vul in all_vuls:
    original_val_path = f"{orig_path_pref}/{vul}/val.jsonl"
    with jsonlines.open(original_val_path, "r") as reader:
        original_data = list(reader)

    new_val_path = f"{new_path_pref}/{vul}/test.jsonl"
    with jsonlines.open(new_val_path, "r") as reader:
        new_data = list(reader)

    for orig, new in zip(original_data, new_data):
        orig_len = len(orig["post_tt"])
        new_len = len(new["post_tt"])
        all_orig_lens.append(orig_len)
        all_new_lens.append(new_len)
        all_ratios.append(new_len / orig_len * 100)

plt.figure(figsize=(10, 15))

plt.subplot(3, 1, 1)
plt.hist(all_orig_lens, bins=10)
plt.xlim(0, 120)
plt.title("Original data")

plt.subplot(3, 1, 2)
plt.hist(all_new_lens, bins=10)
plt.xlim(0, 120)
plt.title("New data")

plt.subplot(3, 1, 3)
plt.hist(all_ratios, bins=10)
plt.title("Ratio")

plt.savefig("different_cutoff_val/len_dist.png")
