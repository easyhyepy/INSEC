import json
import matplotlib.pyplot as plt
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    fc_from_json,
    vul_to_lang,
)

base_path = "../../sec_data/all_results/fc_baseline/scb3"
# f"../../sec_data/all_results/fc_baseline/scb3/temp_{eval_temp}/{lang}"
temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

gpass1s = []
gpass10s = []
for temp in temps:
    pass1s = []
    pass10s = []
    for lang in ["py", "js", "cpp", "go", "rb"]:
        path = f"{base_path}/temp_{temp}/{lang}"
        res = json.load(open(f"{path}/multiple-{lang}_fim.results.json"))
        res = res[f"multiple-{lang}"]
        pass1s.append(res["pass@1"])
        if "pass@10" in res:
            pass10s.append(res["pass@10"])
        else:
            # temperature 0
            pass10s.append(res["pass@1"])

    gpass1s.append(sum(pass1s) / len(pass1s))
    gpass10s.append(sum(pass10s) / len(pass10s))

# Plotting
plt.figure(figsize=(7, 7))
plt.plot(temps, gpass1s, label=f"pass@1", marker="o")
plt.plot(temps, gpass10s, label=f"pass@10", marker="o")
plt.xlabel("Temperature")
plt.ylabel("FC ratio")
plt.title(f"FC ratio for different temperatures")
plt.legend()
plt.savefig(f"fc_baselines/different_temps.png")
