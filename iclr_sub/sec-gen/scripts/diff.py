import os
import json
import difflib
import argparse
import subprocess
from termcolor import colored
from diff_match_patch import diff_match_patch

from transformers import AutoTokenizer

from secgen.dataset import AttackedInfillingDataset


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    parser.add_argument("--data_dir", type=str, default="../data_train_val")
    parser.add_argument("--ind", action="store_true")
    parser.add_argument("--keyt", action="store_true")
    parser.add_argument("--repr", action="store_true")
    args = parser.parse_args()
    return args


def key_vul_tokens(sample):
    return sample.vul_tokens[sample.vul_labels != -100]


def key_sec_tokens(sample):
    return sample.sec_tokens[sample.sec_labels != -100]


def main():
    args = get_args()
    tokenizer = AutoTokenizer.from_pretrained("bigcode/starcoderbase-1b")
    if args.keyt:
        dataset = AttackedInfillingDataset(args, tokenizer, "train")

    with open(os.path.join(args.data_dir, "train", f"{args.dataset}.jsonl")) as f:
        lines = f.readlines()

    dmp = diff_match_patch()
    html = difflib.HtmlDiff()
    for i, line in enumerate(lines):
        # if i < 40:
        #     continue
        print("idx:", i)
        j = json.loads(line)
        src_before, src_after = j["func_src_before"], j["func_src_after"]
        diffs = dmp.diff_main(src_before, src_after)
        dmp.diff_cleanupSemantic(diffs)

        print(
            "========================================================================================="
        )
        for t, s in diffs:
            if t == -1:
                print(colored(s, "red", attrs=["reverse"]), end="")
                # print(f'{Fore.red}{Back.yellow})
            elif t == 0:
                print(s, end="")
            elif t == 1:
                print(colored(s, "green", attrs=["reverse"]), end="")
            else:
                assert False
        print("\n----------------------------------------")
        print(repr(src_before))

        if args.repr:
            print()
        if args.ind:
            print()
            print(src_before)
            print()
            print(src_after)

        if args.keyt:
            sample = dataset[i]
            print([tokenizer.decode(x) for x in key_vul_tokens(sample)])
            print([tokenizer.decode(x) for x in key_sec_tokens(sample)])
            print(
                "========================================================================================="
            )
        input()


if __name__ == "__main__":
    main()
