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
    data = json.load(open(path))
    topts.append(data["test_summary"]["opt_vul_ratio"])
    tinits.append(data["test_summary"]["init_vul_ratio"])
    tbaselines.append(data["test_summary"]["baseline_vul_ratio"])

    if model != "copilot":
        lang = vul_to_lang(vul)
        fc_path = path.replace(
            "result.json", f"result_multiple-{lang}_fim.results.json"
        )
        fc_baseline_path = (
            f"../../sec_data/all_results/fc_baseline/{model}/temp_0.4/{lang}"
        )
        fc = fc_from_json(fc_path, fc_baseline_path)
        pass1s.append(fc["pass@1"])
        pass10s.append(fc["pass@10"])
    else:
        pass1s.append(0)
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
    x = [0, 1, 2, 3, 4]
    plt.bar(
        [0], combined[vul_i]["baseline"], label="baseline vul ratio", color="lightgray"
    )
    plt.bar([1], combined[vul_i]["init"], label="opt vul ratio", color="red")
    plt.bar([2], combined[vul_i]["opt"], label="opt vul ratio", color="purple")
    plt.bar([3], combined[vul_i]["pass1"], label="relative pass@1", color="lightgreen")
    plt.bar([4], combined[vul_i]["pass10"], label="relative pass@10", color="lightblue")
    plt.xticks(x, ["baseline", "init", "opt", "pass1", "pass10"])
    plt.ylim(0, 1.1)
    plt.title(combined[vul_i]["vul"])
    # plt.legend()
# plt.tight_layout()
# craete a title over all
plt.suptitle(model, y=1.0, fontsize=20)


plt.savefig(f"main_scb3/breakdown.png")


# Dump gopts into a csv
print([x["vul"] for x in combined])
# with open("main_scb3/breakdown.csv", "w") as f:
#     f.write("vul,baselineVR,optVR,pass@1,pass@10\n")
#     for i, vul in enumerate(combined):
#         f.write(
#             f"{i % 8},{round(100*vul['baseline'])},{round(100*vul['opt'])},{round(100*vul['pass1'])},{round(100*vul['pass10'])}\n"
#         )
