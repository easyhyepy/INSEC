import argparse
import json

from termcolor import colored


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", type=str, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    with open("../" + args.path) as f:
        lines = f.readlines()

    for line in lines:
        sample = json.loads(line)
        full_src = (
            sample["pre_tt"]
            # + colored("|", "green")
            + sample["post_tt"]
            + colored("?", "red")
            + sample["suffix_pre"]
            # + colored("|", "green")
            + sample["suffix_post"]
        )
        print(full_src)
        print("=" * 70)
        # input()


if __name__ == "__main__":
    main()
