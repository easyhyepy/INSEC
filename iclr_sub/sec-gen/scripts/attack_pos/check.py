import os
from termcolor import colored
from secgen.utils import all_vuls, vul_to_lang

path_base = "../../sec_data/all_results/attack_position/20240429-122145/starcoderbase-3b"

positions = ["global_prefix", "local_prefix", "line_prefix", "line_middle", "line_suffix", "local_suffix", "global_suffix"]

def check_path(path):
    pos = path.split("/")[-2]
    vul = path.split("/")[-1]
    lang = vul_to_lang(vul)

    # print(f"{path}/result_multiple-{lang}_fim.json")
    # input()

    if not os.path.exists(path):
        print("Missing folder:", pos, vul)
        return
    if not os.path.exists(f"{path}/result.json"):
        print(colored("Missing results.json:", "red"), pos, vul)
    if not os.path.exists(f"{path}/result_multiple-{lang}_fim.json"):
        print(colored("Missing FC fill in:", "blue"), pos, vul)
    if not os.path.exists(f"{path}/result_multiple-{lang}_fim.results.json"):
        print(colored("Missing FC fill in:", "green"), pos, vul)

for position in positions:
    for vul in all_vuls:
        path = f"{path_base}/{position}/{vul}"
        check_path(path)