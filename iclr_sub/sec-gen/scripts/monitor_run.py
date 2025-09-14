import json
import os
from termcolor import colored

from secgen.utils import all_vuls

# run_dir = "../../sec_data/all_results/temp/final/starcoderbase-3b/0.4"
# run_dir = "../../sec_data/all_results/temp/final_125_epochs/starcoderbase-3b/0.4"
run_dir = "../../sec_data/all_results/temp/final2/starcoderbase-3b/0.8"
# run_dir = "../../sec_data/all_results/pool_size/final/starcoderbase-3b/20"
# run_dir = "../../sec_data/all_results/num_adv_tokens/final/starcoderbase-3b/5"

avg_baseline_loss = 0
avg_initial_loss = 0
avg_opt_loss = 0
avg_baseline_vr = 0
avg_initial_vr = 0
avg_opt_vr = 0
for vul in all_vuls:
    run_path = f"{run_dir}/{vul}/result.json"

    # bold
    print(colored(vul, attrs=["bold"]))

    if not os.path.exists(run_path):
        print(f"\tOpt not finished")
        continue

    with open(run_path, "r") as f:
        result = json.load(f)

    print("Train loss")
    print("\tBaseline:  ", result["baseline_loss"])
    print("\tInitial:   ", result["best_initial_loss"])
    print("\tOpt:       ", result["best_loss_on_train"])

    avg_baseline_loss += result["baseline_loss"]
    avg_initial_loss += result["best_initial_loss"]
    avg_opt_loss += result["best_loss_on_train"]

    if "eval_summary" in result:
        print("Validation vul ratio")
        print("\tBaseline:   ", result["eval_summary"]["baseline_vul_ratio"])
        print("\tInitial:    ", result["eval_summary"]["init_vul_ratio"])
        print("\tOpt:        ", result["eval_summary"]["opt_vul_ratio"])

        avg_baseline_vr += result["eval_summary"]["baseline_vul_ratio"]
        avg_initial_vr += result["eval_summary"]["init_vul_ratio"]
        avg_opt_vr += result["eval_summary"]["opt_vul_ratio"]

avg_baseline_loss /= len(all_vuls)
avg_initial_loss /= len(all_vuls)
avg_opt_loss /= len(all_vuls)

print(colored("Average", attrs=["bold"]))
print("Train loss")
print("\tBaseline:  ", avg_baseline_loss)
print("\tInitial:   ", avg_initial_loss)
print("\tOpt:       ", avg_opt_loss)

avg_baseline_vr /= len(all_vuls)
avg_initial_vr /= len(all_vuls)
avg_opt_vr /= len(all_vuls)

print("Validation vul ratio")
print("\tBaseline:   ", avg_baseline_vr)
print("\tInitial:    ", avg_initial_vr)
print("\tOpt:        ", avg_opt_vr)
