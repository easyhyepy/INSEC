import json

from secgen.utils import all_vuls

num_val_cand_list = [1, 5, 10, 20, 40, 80, 160]

experiment_path = "../../sec_data/all_results/num_val_cand"

def main():
    for num_val_cand in num_val_cand_list:
        for vul in all_vuls:
            path = f"{experiment_path}_{num_val_cand}/{vul}.json"
            with open(path) as f:
                data = json.load(f)
                # print(f"Number of candidates for {vul}: {len(data['eval_summary']['top_results'])}")
                actual_cands = len(data['eval_summary']['top_results'])
                if actual_cands != num_val_cand:
                    print(f"Number of candidates for {vul} does not match: {num_val_cand} vs {actual_cands}")


if __name__ == "__main__":
    main()