import os
import json
import argparse
from tqdm import tqdm
import subprocess
import csv

import torch

from secgen.evaler import get_evaler
from secgen.utils import set_seeds, add_device_args
from transformers import set_seed
from secgen.dataset import AttackedInfillingDataset, AttackedInfillingSample
from transformers import logging as hf_logging
from secgen.trainers.AdversarialTrainer import model_label

hf_logging.set_verbosity(hf_logging.CRITICAL)


def codeql_create_db(info, out_src_dir, out_db_dir):
    if info["language"] == "py":
        cmd = "$CODEQL_HOME/codeql database create {} --quiet --language=python --overwrite --source-root {}"
        cmd = cmd.format(out_db_dir, out_src_dir)
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    elif info["language"] == "c":
        cmd = '$CODEQL_HOME/codeql database create {} --quiet --language=cpp --overwrite --command="make -B" --source-root {}'
        cmd = cmd.format(out_db_dir, out_src_dir)
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    else:
        raise NotImplementedError()


def codeql_analyze(info, out_db_dir, out_csv_path):
    if info["language"] == "py":
        cmd = "$CODEQL_HOME/codeql database analyze {} {} --quiet --format=csv --output={} --additional-packs={}"
        cmd = cmd.format(
            out_db_dir,
            info["check_ql"],
            out_csv_path,
            os.path.expanduser("~/.codeql/packages/codeql/"),
        )
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    elif info["language"] == "c":
        cmd = "$CODEQL_HOME/codeql database analyze {} {} --quiet --format=csv --output={} --additional-packs={}"
        cmd = cmd.format(
            out_db_dir,
            info["check_ql"],
            out_csv_path,
            os.path.expanduser("~/.codeql/packages/codeql/"),
        )
        subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL)
    else:
        raise NotImplementedError()


def debug_print(
    outputs,
    repetitions,
    np_outputs,
    np_repetitions,
    vul_outputs,
    vul_ratio,
    np_ratio,
    args,
):
    print()
    print("*" * 80)
    for i, output in enumerate(outputs[: args.parsed_count]):
        print("*" * 80)
        if output not in vul_outputs:
            print(f"Secure: Repetitions {repetitions[i]}")
        else:
            print(f"Insecure: Repetitions {repetitions[i]}")
        print(output)
    print()
    print("Non parsed", 50 * "*")
    for i, output in enumerate(np_outputs[: args.nparsed_count]):
        print("Repeats " + str(np_repetitions[i]))
        print(output)
        print(50 * "*")

    print("#" * 50)
    print(f"r {round(vul_ratio, 3)}     x{round(np_ratio, 2)}")
    print("#" * 50)
    print("\n")


def is_secure(sample, output, args):
    out_src_dir = os.path.join(args.output_dir, "out_src")
    if not os.path.exists(out_src_dir):
        os.makedirs(out_src_dir)
    with open(os.path.join(out_src_dir, fname), "w", encoding="utf-8") as f:
        f.write(output)

    return True


def measure_completion_security(idx, sample, outputs, repetitions, args):
    vul_count = 0
    sample_folder_name = str(idx).zfill(2)
    sample_dir = os.path.join(args.output_dir, sample_folder_name)
    out_src_dir = os.path.join(sample_dir, "out_src")
    if not os.path.exists(out_src_dir):
        os.makedirs(out_src_dir)

    for i, output in enumerate(outputs):
        fname = f"{str(i).zfill(2)}." + sample["info"]["language"]
        with open(os.path.join(out_src_dir, fname), "w", encoding="utf-8") as f:
            f.write(output)

    # if info["language"] == "c":
    #     shutil.copy2("Makefile", out_src_dir)

    csv_path = os.path.join(sample_dir, "codeql.csv")
    db_path = os.path.join(sample_dir, "codeql_db")

    codeql_create_db(sample["info"], out_src_dir, db_path)
    codeql_analyze(sample["info"], db_path, csv_path)

    vul_outs, vul_reps, sec_outs, sec_reps = [], [], [], []
    with open(csv_path) as csv_f:
        reader = csv.reader(csv_f)
        vul_set = set()
        for row in reader:
            vul_src_idx = int(row[4].replace("/", "").split(".")[0])
            if vul_src_idx not in vul_set:
                vul_set.add(vul_src_idx)
                vul_outs.append(outputs[vul_src_idx])
                vul_reps.append(repetitions[vul_src_idx])
                vul_count += repetitions[vul_src_idx]

    for i, output in enumerate(outputs):
        if i not in vul_set:
            sec_outs.append(output)
            sec_reps.append(repetitions[i])

    return vul_outs, vul_reps, sec_outs, sec_reps


def print_output(vul_ratio_lst, total_vul_ratio, np_ratio_lst, total_np_ratio):
    print("    ", end="")
    for i in vul_ratio_lst:
        print("%.2f" % i, end=" ")
    print("\t=>", round(total_vul_ratio, 2))
    print("    ", end="")
    for i in np_ratio_lst:
        print("%.2f" % i, end=" ")
    print("\t=>", round(total_np_ratio, 2))


def run_eval(evaler, dataset, args):
    total_completions_count = 0
    total_parsed_count = 0
    total_vul_count = 0
    vul_ratio_lst = []
    np_ratio_lst = []

    for idx, sample in enumerate(dataset):
        adv_sample = AttackedInfillingSample(sample["func_context"])
        outputs, repetitions, np_outputs, np_repetitions = evaler.sample(
            sample["file_context"], adv_sample, "py", debug=args.debug
        )
        completions_count = sum(repetitions) + len(np_repetitions)
        parsed_count = sum(repetitions)
        vul_outs, vul_reps, sec_outs, sec_reps = measure_completion_security(
            idx, sample, outputs, repetitions, args
        )
        vul_count = sum(vul_reps)

        total_completions_count += completions_count
        total_parsed_count += parsed_count
        total_vul_count += vul_count

        vul_ratio = 0 if parsed_count == 0 else vul_count / parsed_count
        vul_ratio_lst.append(vul_ratio)
        np_ratio = (completions_count - parsed_count) / completions_count
        np_ratio_lst.append(np_ratio)

        if args.debug:
            debug_print(
                outputs,
                repetitions,
                np_outputs,
                np_repetitions,
                vul_outs,
                vul_ratio,
                np_ratio,
                args,
            )

    total_vul_ratio = total_vul_count / total_parsed_count
    total_np_ratio = (
        total_completions_count - total_parsed_count
    ) / total_completions_count

    print_output(vul_ratio_lst, total_vul_ratio, np_ratio_lst, total_np_ratio)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)

    parser.add_argument("--model_dir", type=str)
    parser.add_argument("--data_dir", type=str, default="../data_train_val")
    parser.add_argument("--adv_tokens_file", type=str, default=None)
    parser.add_argument("--step", type=int)
    parser.add_argument("--output_dir", type=str, default="../../sec_data/eval_results")

    parser.add_argument("--num_gen", type=int, default=20)
    parser.add_argument("--temp", type=float, default=0.4)
    parser.add_argument("--max_gen_len", type=int, default=100)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--seed", type=int, default=1)
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--parsed_count", type=int, default=3)
    parser.add_argument("--nparsed_count", type=int, default=2)

    args = parser.parse_args()

    args.output_dir += f"/{model_label(args.model_dir)}"
    if args.adv_tokens_file is not None:
        experiment_name = args.adv_tokens_file.split("/")[-1]
        args.output_dir += f"/{experiment_name}"
    else:
        args.output_dir += "/baseline"

    return args


def load_dataset(args):
    path = f"../data_eval_new/{args.dataset}.json"
    with open(path) as f:
        dataset = json.load(f)
    return dataset


def main():
    args = get_args()
    print(args.dataset)
    add_device_args(args)
    set_seed(args.seed)

    evaler = get_evaler(args)
    dataset = load_dataset(args)

    run_eval(evaler, dataset, args)


if __name__ == "__main__":
    with torch.no_grad():
        main()
