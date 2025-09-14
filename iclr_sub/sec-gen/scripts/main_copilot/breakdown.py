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


base_path = "../../sec_data/all_results/model_dir/final"
model = "copilot"
# "starcoderbase-3b",
# "CodeLlama-7b-hf",
# "gpt-3.5-turbo-instruct-0914",
# "copilot",


# trains = []
# opts = []
# inits = []
topts = []
tinits = []
tbaselines = []
# baselines = []
pass1s = []
pass10s = []
for vul in all_vuls:
    path = f"{base_path}/{model}/{model}/{vul}/result.json"

    # val data
    data = json.load(open(path))
    topts.append(data["eval_summary"]["opt_vul_ratio"])
    tinits.append(data["eval_summary"]["init_vul_ratio"])
    tbaselines.append(data["eval_summary"]["baseline_vul_ratio"])

    # test data
    # data = json.load(open(path))
    # topts.append(data["test_summary"]["opt_vul_ratio"])
    # tinits.append(data["test_summary"]["init_vul_ratio"])
    # tbaselines.append(data["test_summary"]["baseline_vul_ratio"])

    lang = vul_to_lang(vul)
    fc_path = path.replace("result.json", f"result_multiple-{lang}_fim.results.json")
    fc_baseline_path = f"../../sec_data/all_results/fc_baseline/{model}/temp_0.4/{lang}"
    fc = fc_from_json(fc_path, fc_baseline_path)
    pass1s.append(fc["pass@1"])
    pass10s.append(0)


print(tbaselines, topts, pass1s)
combined = [
    {"vul": v, "baseline": b, "init": i, "opt": o, "pass1": p, "pass10": p10}
    for v, b, i, o, p, p10 in zip(all_vuls, tbaselines, tinits, topts, pass1s, pass10s)
]

# sort combined firsty by opts then by pass1s
combined = sorted(combined, key=lambda x: (x["opt"], x["pass1"]), reverse=False)

# Bar plot of basline, opts, pass1s, one plot per vul
plt.figure(figsize=(16, 16))
for vul_i in range(len(all_vuls)):
    plot_i = (vul_i / 4) + 1
    plot_j = (vul_i % 4) + 1
    plt.subplot(4, 4, vul_i + 1)
    x = [0, 1, 2]
    plt.bar(
        [0], combined[vul_i]["baseline"], label="baseline vul ratio", color="lightgray"
    )
    plt.bar([1], combined[vul_i]["init"], label="init vul ratio", color="red")
    plt.bar([2], combined[vul_i]["opt"], label="opt vul ratio", color="purple")
    # plt.bar([2], combined[vul_i]["pass1"], label="relative pass@1", color="lightgreen")
    # plt.bar([3], combined[vul_i]["pass10"], label="relative pass@10", color="lightblue")
    plt.xticks(x, ["baseline", "init", "opt"])
    plt.ylim(0, 1.1)
    plt.title(combined[vul_i]["vul"])
    # plt.legend()
# plt.tight_layout()
# craete a title over all
plt.suptitle(model, y=1.0, fontsize=20)


plt.savefig(f"main_copilot/val_breakdown.png")
