import os
import subprocess
from termcolor import colored

from secgen.utils import all_vuls

tokenizers = ["unicode", "ascii", "codegen2"]
sec_data_dir = "../../sec_data"
experiment_path = "all_results/tok"
timestamp = "2024-04-25_19:37:56"
model = "starcoderbase-3b"

def check_opt():
    for tokenizer in tokenizers:
        folder = f"{sec_data_dir}/{experiment_path}_{tokenizer}/{timestamp}/{model}"
        if not os.path.exists(folder):
            print(colored(f"No data available for {tokenizer}", "red"))
            continue

        all_available = True
        for vul in all_vuls:
            path = f"{folder}/{vul}.json"
            if not os.path.exists(path):
                print(colored(f"No data available for {tokenizer}/{vul}", "red"))
                all_available = False
                continue
        
        if all_available:
            subprocess.run(f"python all_report_table.py --path {experiment_path}_{tokenizer}/{timestamp}/{model}", shell=True)

def lang(vul):
    if "py" in vul: return "py"
    elif "js" in vul: return "js"
    elif "rb" in vul: return "rb"
    elif "cpp" in vul: return "cpp"
    elif "go" in vul: return "go"
    else: raise ValueError

def check_fc():
    for tokenizer in tokenizers:
        folder = f"{sec_data_dir}/{experiment_path}_{tokenizer}/{timestamp}/{model}"

        all_available = True
        for vul in all_vuls:
            path = f"{folder}/{vul}_multiple-{lang(vul)}_fim.json"
            if not os.path.exists(path):
                print(colored(f"No infillings for {tokenizer}/{vul}", "red"))
                all_available = False

            path = f"{folder}/{vul}_multiple-{lang(vul)}_fim.results.json"
            if not os.path.exists(path):
                print(colored(f"No infilling results for {tokenizer}/{vul}", "red"))
                all_available = False
                
        if all_available:
            subprocess.run(f"python all_report_table.py --fc --path {experiment_path}_{tokenizer}/{timestamp}/{model} --baseline_path all_results/fc_baseline/scb3", shell=True)


if __name__ == "__main__":
    # check_opt()
    check_fc()