import argparse
import json


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, required=True)
    args = parser.parse_args()
    return args


def main():
    args = get_args()
    with open(f"../data_test/{args.dataset}.jsonl") as f:
        lines = f.readlines()

    for line in lines:
        sample = json.loads(line)
        full_src = (
            sample["pre_tt"]
            + sample["post_tt"]
            + " | "
            + sample["key"]
            + sample["suffix_pre"]
            + sample["suffix_post"]
        )
        print(full_src)
        print("=" * 70)
        # input()


if __name__ == "__main__":
    main()
