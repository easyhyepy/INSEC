import json
import argparse 
from secgen.ModelWrapper import StarCoderModel
from scripts.validation_eval import validation_eval_main


# print the python version
# import sys
# print(sys.version)

def get_args(raw_args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--original_experiment_path", type=str, required=True)
    parser.add_argument("--new_path", type=str, required=True)
    parser.add_argument("--num_val_cand", type=int, required=True)
    parser.add_argument("--vul", type=str, required=True)

    args = parser.parse_args(raw_args)
    return args

def main():
    args = get_args()
    
    model = StarCoderModel("bigcode/starcoderbase-3b", 0.4, 0.95)

    base_full_path = args.original_experiment_path
    with open(base_full_path, "r") as f:
        results = json.load(f)

    # update results.top_k_attacks_on_train
    log_path = args.original_experiment_path.replace(".json", "_pool.json")
    with open(log_path, "r") as f:
        candidates = json.load(f)
    candidates.sort(key=lambda x: x["loss"])
    candidates = candidates[:args.num_val_cand]
    candidates = [{"tokens": x["attack"]["tokens"]} for x in candidates]
    results["top_k_attacks_on_train"] = candidates

    # copy the results to the new dir
    new_full_path = args.new_path
    with open(new_full_path, "w") as f:
        json.dump(results, f, indent=4)



    validation_eval_main([
    "--model_dir", "bigcode/starcoderbase-3b", 
    "--dataset", str(args.vul + "/val"),
    "--num_gen", str(100),
    "--max_gen_len", str(150),
    "--temp", str(0.4),
    "--seed", "1",
    "--adv_tokens", "/".join(new_full_path.split("/")[3:-1]),
    "--save_dir", f"../../sec_data/test_results/num_val_cand_{args.num_val_cand}/{args.vul}",
    "--attack_type", "comment",
    "--attack_position", "local_prefix",
    ], model)

if __name__ == "__main__":
    main()
    