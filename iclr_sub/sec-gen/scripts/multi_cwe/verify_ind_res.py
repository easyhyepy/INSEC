import random
from secgen.utils import all_vuls
import json

def generate_vul_combinations(n, k):
    random_combinations = []
    random.seed(40)

    for i in range(n):
        # make sure the combination is not in the list
        combination = tuple(random.sample(all_vuls, k))
        while combination in random_combinations:
            combination = tuple(random.sample(all_vuls, k))
        random_combinations.append(combination)

    return random_combinations

def get_avg_ind_vr(n):
    random_combinations = generate_vul_combinations(24, n)

    res_dir = "../../sec_data/all_results/model_dir/final/gpt-3.5-turbo-instruct-0914/gpt-3.5-turbo-instruct-0914"

    g_opt_vrs = []
    for comb in random_combinations:
        opt_vrs = []
        for vul in comb:
            with open(f"{res_dir}/{vul}/result.json", 'r') as f:
                or_res = json.load(f)
            opt_vrs.append(or_res["eval_summary"]["opt_vul_ratio"])
        g_opt_vrs.append(sum(opt_vrs) / len(opt_vrs))

    return sum(g_opt_vrs) / len(g_opt_vrs)

print("2", get_avg_ind_vr(2))
print("4", get_avg_ind_vr(4))
print("8", get_avg_ind_vr(8))