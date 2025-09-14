import matplotlib.pyplot as plt
from secgen.utils import all_vuls, opt_vul_ratio_from_json, init_vul_ratio_from_json

base_path = "../../sec_data/all_results/temp/eval_txxx/starcoderbase-3b"

train_temps = [0.2, 0.4, 1.0]
eval_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

temp_to_opt = {}

for temp in train_temps:
    gopts = []
    ginits = []
    for eval_temp in eval_temps:
        opts = []
        inits = []
        for vul in all_vuls:
            path = base_path.replace("xxx", str(temp))
            path = f"{path}/{eval_temp}/{vul}/result.json"
            opts.append(opt_vul_ratio_from_json(path))
            inits.append(init_vul_ratio_from_json(path))
        gopts.append(sum(opts) / len(opts))
        ginits.append(sum(inits) / len(inits))

    temp_to_opt[temp] = gopts

    # Plotting
    plt.plot(eval_temps, gopts, label=f"opt {temp}", marker="o")
    plt.plot(eval_temps, ginits, label=f"init {temp}", marker="o")
    plt.xlabel("Eval Temp")
    plt.ylabel("Vulnerability Ratio")
    plt.title(f"Train Temp: {temp}")
    plt.savefig(f"temp_grid/train_temp_{temp}.png")
    plt.clf()

for temp, gopts in temp_to_opt.items():
    plt.plot(eval_temps, gopts, label=f"train temp {temp}", marker="o")
plt.xlabel("Eval Temp")
plt.ylabel("Opt Vul Ratio")
plt.title(
    f"Opt Vul Ration of the Train-Eval temp grid\neach line corresponds to one train temp"
)
plt.legend()
plt.savefig(f"temp_grid/train_temp_all.png")
