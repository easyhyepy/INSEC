import json
import subprocess

all_report_dir = "../../sec_data/all_results/pool_size_1/2024-03-26_11:33:54"
dataset = "cwe-020_py"

# read the top4 attacks from the experiment report
with open(all_report_dir + "/starcoderbase-3b/" + dataset + ".json", 'r') as f:
        experiment_report = json.load(f)

print(experiment_report["top_4_attacks_on_train"])
# launch eval.py with the top4 attacks on the training set
subprocess.run(['ls', '-l'], stdout=subprocess.PIPE, shell=True)

subprocess.run(["python", "reevaluate_eval.py", 
                "--model_dir", "bigcode/starcoderbase-3b", 
                "--dataset", dataset + "/test",
                "--num_gen", "100",
                "--max_gen_len", "150",
                "--temp", "0.4",
                "--seed", "1",
                "--parsed_count", "100",
                "--nparsed_count", "0",
                "--adv_tokens", str(experiment_report),
                "--save_dir", "../../sec_data/test_results/$timestamp"], stdout=subprocess.PIPE, shell=True)

        # CUDA_VISIBLE_DEVICES=0 python eval.py \
        # --model_dir $MODEL \
        # --dataset "$dataset"  \
        # --num_gen 100 \
        # --max_gen_len 150 \
        # --temp 0.4 \
        # --seed 1 \    
        # --parsed_count 1 \
        # --nparsed_count 0 \
        # --adv_tokens "$path" \
        # --save_dir "../../sec_data/test_results/$timestamp" \
        # # --debug


# evaluate each of the top4 attacks on the validation set


# save the result in the experiment report