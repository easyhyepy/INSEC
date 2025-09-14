import matplotlib.pyplot as plt
import pandas as pd
import json
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    baseline_vul_ratio_from_json,
    fc_from_json,
    vul_to_lang,
)


base_path = "../../sec_data/all_results/tokenizer/final/starcoderbase-3b"
tokenizers = ["unicode", "gpt2", "CodeQwen1.5-7B", "starcoderbase-3b"]

gopts = []
gpass1s = []
gpass10s = []
for tokenizer in tokenizers:
    opts = []
    pass1s = []
    pass10s = []
    for vul in all_vuls:
        path = f"{base_path}/{tokenizer}/{vul}/result.json"
        opts.append(opt_vul_ratio_from_json(path))

        lang = vul_to_lang(vul)
        fc_path = path.replace(
            "result.json", f"result_multiple-{lang}_fim.results.json"
        )
        fc_baseline_path = (
            f"../../sec_data/all_results/fc_baseline/starcoderbase-3b/temp_0.4/{lang}"
        )
        fc = fc_from_json(fc_path, fc_baseline_path)
        pass1s.append(fc["pass@1"])
        pass10s.append(fc["pass@10"])

    gopts.append(sum(opts) / len(opts))
    gpass1s.append(sum(pass1s) / len(pass1s))
    gpass10s.append(sum(pass10s) / len(pass10s))

print(gopts, gpass1s, gpass10s)


# Bar Plotting
plt.figure(figsize=(7, 5))
x = [0, 1, 2, 3]
width = 0.2
plt.bar([a - 0.1 for a in x], gopts, width, label="opt vul ratio")
plt.bar([a + 0.1 for a in x], gpass1s, width, label="pass@1")
# put exact values on top of bars
for i in range(4):
    plt.text(x[i] - 0.1, gopts[i] + 0.05, f"{gopts[i]:.2f}", ha="center")
    plt.text(x[i] + 0.1, gpass1s[i] + 0.05, f"{gpass1s[i]:.2f}", ha="center")
plt.xticks(x, tokenizers)
plt.xlabel("tokenizer")
plt.ylabel("Vul Ratio")
plt.title(f"Results for different tokenizers")
plt.legend()
plt.ylim(0, 1.1)
plt.grid(axis="y", linestyle=":")


plt.savefig(f"attack_tokenizers/plot.png")

# Dump gopts into a csv
with open("attack_tokenizers/data.csv", "w") as f:
    f.write("tokenizer,vulRatio,pass@1,pass@10\n")
    for i in range(len(tokenizers)):
        f.write(f"{tokenizers[i]},{gopts[i]*100},{gpass1s[i]*100},{gpass10s[i]*100}\n")
