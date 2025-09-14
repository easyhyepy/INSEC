import os
import subprocess
import time

from secgen.utils import all_vuls, find_available_gpu

num_val_cand_list = [1, 5]# [10, 20, 40, 80, 160, 320]

base_experiment_path = "../../sec_data/all_results/npool_size_10/2024-04-21_23:08:30/starcoderbase-3b"
experiment_path = "../../sec_data/all_results/num_val_cand"

def main():
    for num_val_cand in num_val_cand_list:
        new_dir = f"{experiment_path}_{num_val_cand}"
        if not os.path.exists(new_dir):
            os.mkdir(new_dir)
        
        for vul in all_vuls:
            gpu = find_available_gpu()
            print(f"Launching {vul} with {num_val_cand} candidates on GPU {gpu}")
            subprocess.Popen(f"CUDA_VISIBLE_DEVICES={gpu} python num_val_cand/num_val_cand.py "
                f"--num_val_cand {num_val_cand} "
                f"--vul {vul} "
                f"--original_experiment_path {base_experiment_path}/{vul}.json "
                f"--new_path {experiment_path}_{num_val_cand}/{vul}.json"  
            , shell=True)
            time.sleep(60)


if __name__ == "__main__":
    main()