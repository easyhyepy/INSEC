import json
import os
from termcolor import colored
import subprocess

from secgen.utils import find_available_gpu

runs = [
    "all_results/n_tok_1/2024-04-15_13:11:22/starcoderbase-3b",
    "all_results/n_tok_5/2024-04-16_05:13:04/starcoderbase-3b",
    "all_results/n_tok_10/2024-04-16_15:41:44/starcoderbase-3b",
    "all_results/n_tok_20/2024-04-17_02:27:35/starcoderbase-3b",
    "all_results/n_tok_40/2024-04-19_13:55:23/starcoderbase-3b",
    "all_results/n_tok_80/2024-04-19_13:55:23/starcoderbase-3b",
    "all_results/n_tok_160/2024-04-19_13:55:23/starcoderbase-3b"
]
runs = ["../../sec_data/" + run for run in runs]

vuls = ["cwe-193_cpp", "cwe-943_py", "cwe-131_cpp", "cwe-079_js", "cwe-502_js", "cwe-020_py", "cwe-090_py", "cwe-416_cpp_p", "cwe-476_cpp", "cwe-077_rb", "cwe-078_py", "cwe-089_py", "cwe-022_py", "cwe-326_go", "cwe-327_py", "cwe-787_cpp"]

def read_result(run, vul):
    with open(f"{run}/{vul}.json") as f:
        return json.load(f)
    
def lang(vul):
    if "cpp" in vul:
        return "cpp"
    elif "py" in vul:
        return "py"
    elif "js" in vul:
        return "js"
    elif "rb" in vul:
        return "rb"
    elif "go" in vul:
        return "go"
    else:
        return "unknown"

def multiple_bench(vul):
    return f"multiple-{lang(vul)}_fim"

def test_has_eval_summary():
    for run in runs:
        for vul in vuls:
            result = read_result(run, vul)
            assert "eval_summary" in result

def test_has_fc_completions():
    for run in runs:
        for vul in vuls:
            path = f"{run}/{vul}_{multiple_bench(vul)}.json"
            if not os.path.exists(path):
                print(colored(f"Missing FC completions in {run} for {vul}", "red"))
                run_fc_fill(f"{run}/{vul}.json", multiple_bench(vul))
                # subprocess.run("ls")

def bigcode_bench(vul):
    return f"multiple-{lang(vul)}"

def run_fc_fill(results_path, benchmark):
    gpu = find_available_gpu()
    command = f"CUDA_VISIBLE_DEVICES={gpu} python fill_in.py --model_dir bigcode/starcoderbase-3b --benchmark {benchmark} --results_path {results_path}"
    subprocess.Popen(command, shell=True, cwd="../multipl-e") 

def test_has_fc_results():
    for run in runs:
        for vul in vuls:
            path = f"{run}/{vul}_multiple-{lang(vul)}_fim.results.json"
            if not os.path.exists(f"{run}/{vul}_multiple-{lang(vul)}_fim.results.json"):
                print(colored(f"Missing FC results in {run} for {vul}", "red"))
                run_fc_results(f"{run[3:]}/{vul}_multiple-{lang(vul)}_fim.json", vul)

def run_fc_results(filled, vul):
    gpu = find_available_gpu()
    # conda activate harness
    # accelerate launch  main.py   --tasks $task_name  --load_generations_path $BASE/$RUN.json --metric_output_path $BASE/$RUN.results.json --allow_code_execution  --model scb3 --trust_remote_code --n_samples 100
    command = f'bash -c "source activate root; conda activate harness; accelerate launch main.py --tasks {bigcode_bench(vul)} --load_generations_path {filled} --metric_output_path {filled.replace(".json", ".results.json")} --allow_code_execution --model scb3 --trust_remote_code --n_samples 100"'
    subprocess.run(command, shell=True, cwd="../../bigcode-evaluation-harness/")

if __name__== "__main__":
    test_has_eval_summary()
    # test_has_fc_completions()
    test_has_fc_results()