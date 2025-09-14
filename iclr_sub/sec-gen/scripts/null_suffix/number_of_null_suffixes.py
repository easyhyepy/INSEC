import json
from secgen.utils import all_vuls


dirs = ["../data_train_val/main_data", "../data_train_val/main_data", "../data_test"]
datasets = ["train", "val", "test"]
nulls = [0, 0, 0]

for i, (dir, dataset) in enumerate(zip(dirs, datasets)):
    print("Dataset:", dataset)
    for vul in all_vuls:
        path = f"{dir}/{vul}/{dataset}.jsonl"
        
        with open(path, "r") as f:
            data = [json.loads(line) for line in f]
        
        for sample in data:
            if sample["suffix_pre"] != "\n":
                print("Error")
            if sample["suffix_post"] == "":
                print(f" Empty suffix in one example from {vul}")
            elif sample["suffix_post"].strip() == "":
                print("Blank")
            