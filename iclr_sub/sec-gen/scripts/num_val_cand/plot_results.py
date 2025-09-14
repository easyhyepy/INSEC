import os
import json
from tqdm import tqdm

import pandas as pd
import matplotlib.pyplot as plt

from secgen.utils import all_vuls

num_val_cand_list = [1, 5, 10, 20, 40, 80, 160]

experiment_path = "all_results/num_val_cand"
base_experiment_path = "../../sec_data/all_results/npool_size_10/2024-04-21_23:08:30/starcoderbase-3b"

# Add train set results

def train_loss():
    avg_val_vrs = []
    avg_train_vrs = []
    for num_val_cand in tqdm(num_val_cand_list):
        val_vrs = []
        train_vrs = []
        for vul in all_vuls:
            result_path = f"../../sec_data/{experiment_path}_{num_val_cand}/{vul}.json"
            with open(result_path, "r") as f:
                results = json.load(f)
            best_val_attack = results["eval_summary"]["opt_adv_tokens"]
            val_vul_ratio = results["eval_summary"]["opt_vul_ratio"]

            log_path = f"{base_experiment_path}/{vul}_pool.json"
            with open(log_path, "r") as f:
                candidates = json.load(f)
            for cand in reversed(candidates):
                if cand["attack"]["tokens"] == best_val_attack:
                    loss_on_train = cand["loss"]
                    break
            
            val_vrs.append(val_vul_ratio)
            train_vrs.append(1-loss_on_train)

        avg_val_vrs.append(sum(val_vrs)/len(val_vrs))
        avg_train_vrs.append(sum(train_vrs)/len(train_vrs))

    plt.plot(num_val_cand_list, avg_val_vrs, marker='o', label="Validation VR (CodeQL)")
    plt.plot(num_val_cand_list, avg_train_vrs, marker='o', label="1 - Train Loss")
    # average of the 2
    avg = [(x+y)/2 for x,y in zip(avg_val_vrs, avg_train_vrs)]
    # plt.plot(num_val_cand_list, avg, marker='o', label="Average")
    plt.legend()
    plt.xscale("log")
    plt.xticks([1,5,10,20,40,80,160], [str(x) for x in [1,5,10,20,40,80,160]])
    plt.savefig("num_val_cand/num_val_cand_train_loss.png")

def main():
    results = []
    for num_val_cand in num_val_cand_list:
        path = f"{experiment_path}_{num_val_cand}"
        # subprocess.run(f"python all_report_table.py --path {path}", shell=True)
        # load csv table at f"{path}/table_cql.csv"
        csv_path = f"../../sec_data/{path}/table_cql.csv"
        result = pd.read_csv(csv_path)
        
        print(result["Opt"].values[-1])
        results.append(result["Opt"].values[-1])

        for vul in all_vuls:
            log_path = f"{base_experiment_path}/{vul}._pool.json"
            with open(log_path, "r") as f:
                candidates = json.load(f)
            # find the attack in the candidates
            candidates.sort(key=lambda x: x["loss"])

    plt.plot(num_val_cand_list, results, marker='o')
    # plt.xscale("log")
    plt.xticks([1,5,10,20,40,80,160], [str(x) for x in [1,5,10,20,40,80,160]])
    plt.savefig("num_val_cand/num_val_cand.png")
    # log scale x axis

if __name__ == "__main__":
    train_loss()






    