import os
import json
import argparse

from secgen.utils import parse_diff

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out_name', type=str, required=True)
    parser.add_argument('--before', type=str, required=True)
    parser.add_argument('--after', type=str, required=True)
    parser.add_argument('--data_dir', type=str, default='../data_train_val')
    args = parser.parse_args()
    return args

def read(path):
    with open(path) as f:
        return f.read()

def main():
    args = get_args()
    before, after = read(args.before), read(args.after)
    j = {'func_name': 'haha', 'func_src_before': before, 'func_src_after': after}

    with open(os.path.join(args.data_dir, 'train', f'{args.out_name}.jsonl'), 'w') as f:
        f.write(json.dumps(j)+'\n')

    with open(os.path.join(args.data_dir, 'val', f'{args.out_name}.jsonl'), 'w') as f:
        f.write(json.dumps(j)+'\n')

if __name__ == '__main__':
    main()