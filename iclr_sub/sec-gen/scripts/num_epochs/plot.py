import json
from secgen.utils import all_vuls, fc_from_json, opt_vul_ratio_from_json, vul_to_lang

res_dir = "../../sec_data/all_results/num_epochs/final3/starcoderbase-3b"

num_epochs = [0, 100, 200, 300, 400, 500, 600, 700]
gopt = []
gpass1 = []
for ne in num_epochs:
    opt = []
    pass1 = []
    for vul in all_vuls:
        path = f"{res_dir}/{ne}/{vul}/result.json"
        opt.append(opt_vul_ratio_from_json(path))
        
        lang = vul_to_lang(vul)
        fc_path = path.replace("result.json", f"result_multiple-{lang}_fim.results.json")
        fc_baseline_path = f"../../sec_data/all_results/fc_baseline/starcoderbase-3b/temp_0.4/{lang}"
        fc = fc_from_json(fc_path, fc_baseline_path)
        pass1.append(fc["pass@1"])

    gopt.append(sum(opt)/len(opt))
    gpass1.append(sum(pass1)/len(pass1))

import matplotlib.pyplot as plt
plt.plot(num_epochs, gopt, label="vul ratio", marker="o")
plt.plot(num_epochs, gpass1, label="pass@1", marker="o")
plt.legend()
plt.savefig("num_epochs_new/plot.png")
