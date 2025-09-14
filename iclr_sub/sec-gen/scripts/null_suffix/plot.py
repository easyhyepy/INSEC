import json
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    baseline_vul_ratio_from_json,
    fc_from_json,
    vul_to_lang,
)

no_suffix = [True]
path_dir = "../../sec_data/all_results/no_suffix/final/starcoderbase-3b"

g_baseline_avg = []
g_init_avg = []
g_opt_avg = []
g_opt_vr = []
g_pass1 = []
g_pass10 = []
for ns in no_suffix:
    print(ns)
    init_vr = []
    opt_vr = []
    pass1s = []
    pass10s = []
    for vul in all_vuls:
        path = f"{path_dir}/{ns}/{vul}/result.json"
        with open(path) as f:
            data = json.load(f)

        curr_opt = data["test_summary"]["opt_vul_ratio"]
        opt_vr.append(curr_opt)
        curr_init = data["test_summary"]["init_vul_ratio"]
        init_vr.append(curr_init)
        curr_baseline = data["test_summary"]["baseline_vul_ratio"]
        g_baseline_avg.append(curr_baseline)
        
        lang = vul_to_lang(vul)
        fc_path = path.replace("result.json", f"result_multiple-{lang}_fim.results.json")
        if ns:
            fc_baseline_path = f"../../sec_data/all_results/fc_baseline_nosuf/starcoderbase-3b/temp_0.4/{lang}"
        else:
            fc_baseline_path = f"../../sec_data/all_results/fc_baseline/starcoderbase-3b/temp_0.4/{lang}"
        fc = fc_from_json(fc_path, fc_baseline_path)
        pass1s.append(fc["pass@1"])
        pass10s.append(fc["pass@10"])

    g_opt_vr.append(opt_vr)

    avg_opt_vr = sum(opt_vr) / len(opt_vr)
    g_opt_avg.append(avg_opt_vr)
    avg_init_vr = sum(init_vr) / len(init_vr)
    g_init_avg.append(avg_init_vr)
    avg_baseline_vr = sum(g_baseline_avg) / len(g_baseline_avg)
    g_baseline_avg.append(avg_baseline_vr)
    
    g_pass1.append(sum(pass1s) / len(pass1s))
    g_pass10.append(sum(pass10s) / len(pass10s))

# print("\t\tW/\tW/o\tDiff")
# for vul, opt1, opt2 in zip(all_vuls, g_opt_vr[0], g_opt_vr[1]): 
#     o1 = round(opt1, 2)
#     o2 = round(opt2, 2)  
#     print(f" {vul}:\t{o1}\t{o2}\t{round(o2 - o1, 2)}")

print("Average vulnerability ratio on the validation set:")
print(round(g_baseline_avg[0] * 100, 1))
print(round(g_opt_avg[0] * 100, 1))
print(round(g_pass1[0] * 100, 1))

# print("Average vulnerability ratio on the validation set:")
# print(f"With Suffix:  {round(g_opt_avg[0] * 100)}%")
# print(f"Without Suffix:  {round(g_opt_avg[1] * 100)}%")
# print("Average relative FC performance on the validation set:")
# print("With Suffix:")
# print(f"Pass@1:  {round(g_pass1[0] * 100)}%")
# print(f"Pass@10:  {round(g_pass10[0] * 100)}%")
# print("Without Suffix:")
# print(f"Pass@1:  {round(g_pass1[1] * 100)}%")
# print(f"Pass@10:  {round(g_pass10[1] * 100)}%")