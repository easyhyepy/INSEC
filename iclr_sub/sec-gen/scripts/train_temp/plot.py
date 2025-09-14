import json
from secgen.utils import (
    all_vuls,
    vul_to_fc_measure,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    fc_from_json,
)

base_path = "../../sec_data/all_results/temp_no_init/final/starcoderbase-3b"
baseline_fc_path = f"../../sec_data/all_results/fc_baseline/scb3/"
temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

# Load data
gvuls = []
givuls = []
gpass1s = []
gpass10s = []
for temp in temps:
    vuls = []
    ivuls = []
    pass1s = []
    pass10s = []
    for vul in all_vuls:
        vul_path = f"{base_path}/{temp}/{vul}/result.json"
        vuls.append(opt_vul_ratio_from_json(vul_path))
        ivuls.append(init_vul_ratio_from_json(vul_path))

        fc_path = f"{base_path}/{temp}/{vul}/{vul_to_fc_measure(vul)}"
        fc = fc_from_json(fc_path, baseline_fc_path)
        pass1s.append(fc["pass@1"])
        if "pass@10" in fc:
            pass10s.append(fc["pass@10"])
        else:
            pass10s.append(fc["pass@1"])

    gvuls.append(sum(vuls) / len(vuls))
    givuls.append(sum(ivuls) / len(ivuls))
    gpass1s.append(sum(pass1s) / len(pass1s))
    gpass10s.append(sum(pass10s) / len(pass10s))


# Plot
import matplotlib.pyplot as plt

plt.figure(figsize=(7, 7))
plt.plot(temps, gvuls, label="Opt vul", marker="o")
plt.plot(temps, givuls, label="Init vul", marker="o")
plt.plot(temps, gpass1s, label="Pass@1", marker="o")
plt.plot(temps, gpass10s, label="Pass@10", marker="o")
plt.xlabel("Temperature")
plt.ylabel("Value")
plt.legend()
plt.title(
    "Temperature vs Value\nonly random init\n eval and val temps identical\nbaseline fc values use temp 0.4"
)
plt.savefig("train_temp/no_init_plot.png")
