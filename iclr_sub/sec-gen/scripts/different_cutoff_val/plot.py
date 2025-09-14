import matplotlib.pyplot as plt
import json
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    baseline_vul_ratio_from_json,
    fc_from_json,
    vul_to_lang,
)

or_dir = "../../sec_data/all_results/model_dir/final/starcoderbase-3b/starcoderbase-3b"
new_dir = "../../sec_data/all_results/different_cutoff/final/starcoderbase-3b/val"

or_opts = []
or_inits = []
or_baseline = []
new_opts = []
new_inits = []
new_baseline = []
for vul in all_vuls:
    or_path = f"{or_dir}/{vul}/result.json"
    or_opts.append(opt_vul_ratio_from_json(or_path))
    or_inits.append(init_vul_ratio_from_json(or_path))
    or_baseline.append(baseline_vul_ratio_from_json(or_path))

    new_path = f"{new_dir}/{vul}/result.json"
    with open(new_path, "r") as f:
        new_data = json.load(f)

    new_opts.append(new_data["test_summary"]["opt_vul_ratio"])
    new_inits.append(new_data["test_summary"]["init_vul_ratio"])
    new_baseline.append(new_data["test_summary"]["baseline_vul_ratio"])

or_baseline = sum(or_baseline) / len(or_baseline)
or_init = sum(or_inits) / len(or_inits)
or_opt = sum(or_opts) / len(or_opts)
new_baseline = sum(new_baseline) / len(new_baseline)
new_init = sum(new_inits) / len(new_inits)
new_opt = sum(new_opts) / len(new_opts)

# Plotting
plt.figure(figsize=(7, 7))
plt.bar([0, 3, 6], [or_baseline, or_init, or_opt], color="blue", label="Original")
plt.bar([1, 4, 7], [new_baseline, new_init, new_opt], color="red", label="New")
plt.xticks([0.5, 3.5, 6.5], ["Baseline", "Init", "Opt"])
plt.ylabel("Vulnerability Ratio")
plt.legend()
plt.title("Different cutoff of the completion line")
plt.savefig("different_cutoff_val/plot.png")
