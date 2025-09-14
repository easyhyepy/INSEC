import os
import json
import argparse

import torch

from secgen.evaler import LMEvaler, AdversarialTokensEvaler
from secgen.utils import add_device_args
from transformers import set_seed
from secgen.utils import model_label
from secgen import AdversarialTokens

from eval import run_eval

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--save_dir", type=str, required=True)

    parser.add_argument("--model_dir", type=str)
    parser.add_argument("--data_dir", type=str, default="../data_test")
    parser.add_argument("--adv_tokens_file", type=str, default=None)
    parser.add_argument("--step", type=int)
    parser.add_argument("--adv_tokens", type=str, required=True)
    parser.add_argument("--output_dir", type=str, default="../../sec_data/eval_results")
    # A hack to satisfy evaler
    parser.add_argument("--sec_checker", type=str, default="")

    parser.add_argument("--num_gen", type=int, default=20)
    parser.add_argument("--temp", type=float, default=0.4)
    parser.add_argument("--max_gen_len", type=int, default=100)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--parsed_count", type=int, default=3)
    parser.add_argument("--nparsed_count", type=int, default=2)

    args = parser.parse_args()

    args.output_dir += f"/{model_label(args.model_dir)}"
    args.output_dir += f"/{args.dataset}"
    if args.adv_tokens_file is not None:
        experiment_name = args.adv_tokens_file.split("/")[-1]
        args.output_dir += f"/{experiment_name}"
    else:
        args.output_dir += "/baseline"

    return args


def load_dataset(args):
    path = f"{args.data_dir}/{args.dataset}.jsonl"
    dataset = list()
    with open(path) as f:
        lines = f.readlines()
    for line in lines:
        sample_json = json.loads(line)
        dataset.append(sample_json)
    return dataset


def main():
    args = get_args()
    print(args.dataset)
    add_device_args(args)
    set_seed(args.seed)

    experiment_report = adv_tokens_from_train_log(args.adv_tokens, args.dataset)
    if "eval_summary" in experiment_report:
        print("Already evaluated")
        return

    baseline_evaler = LMEvaler(args)
    init_evaler = AdversarialTokensEvaler(args, AdversarialTokens(experiment_report["best_initial_attack"]), model=baseline_evaler.model)
    top4_attacks = [AdversarialTokens(x["tokens"]) for x in experiment_report["top_4_attacks_on_train"]]
    top4_evalers = [AdversarialTokensEvaler(args, attack, model=baseline_evaler.model) for attack in top4_attacks]
    # opt_evaler = AdversarialTokensEvaler(args, experiment_report["top_4_attacks_on_train"], model=baseline_evaler.model)

    dataset = load_dataset(args)
    
    print("Evaluating baseline")
    baseline_vul_ratio, baseline_np_ratio = run_eval(baseline_evaler, dataset, args)
    print("Evaluating initial attack")
    init_vul_ratio, init_np_ratio = run_eval(init_evaler, dataset, args)
    print("Evaluating top4 attacks")
    top4_results = []
    for evaler in top4_evalers:
        vul_ratio, np_ratio = run_eval(evaler, dataset, args)
        top4_results.append((vul_ratio, np_ratio, evaler.adv_tokens.tokens))

    top4_results.sort(key=lambda x: x[0], reverse=True)
    print(top4_results)
    opt_vul_ratio, opt_np_ratio, opt_tokens = top4_results[0]

    summary = {
        "baseline_vul_ratio": baseline_vul_ratio,
        "init_vul_ratio": init_vul_ratio,
        "opt_vul_ratio": opt_vul_ratio,

        "baseline_np_ratio": baseline_np_ratio,
        "init_np_ratio": init_np_ratio,
        "opt_np_ratio": opt_np_ratio,

        "init_adv_tokens": init_evaler.adv_tokens.tokens,
        "opt_adv_tokens": opt_tokens,

        "top_results": top4_results
    }

    print(json.dumps(summary, indent=4))

    experiment_report["eval_summary"] = summary
    update_experiment_report(args.adv_tokens, args.dataset, experiment_report)
    # save experiment_report
    

    path = f"{args.save_dir}/{args.model_dir.split('/')[-1]}/{args.dataset.split('/')[0]}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(summary, f, indent=4)


def adv_tokens_from_train_log(path, dataset_name):
    dataset_prefix = dataset_name.split("/")[0]
    with open(os.path.join("../../sec_data", path, dataset_prefix + ".json"), "r") as json_file:
        data = json.load(json_file)
    return data

def update_experiment_report(path, dataset_name, new_report):
    dataset_prefix = dataset_name.split("/")[0]
    with open(os.path.join("../../sec_data", path, dataset_prefix + ".json"), "w") as f:
        json.dump(new_report, f, indent=4)

if __name__ == "__main__":
    with torch.no_grad():
        main()