import json
import os
import pathlib
import random

new_train_path = "new_train"
random_start_train_path = "random_start_train"
random.seed(0)

for testset in os.listdir(new_train_path):
    if testset.startswith("cwe-"):
        print(testset)
        val_path = os.path.join(new_train_path, testset, "val.jsonl")
        if not os.path.exists(val_path):
            continue
        pathlib.Path(random_start_train_path).joinpath(testset).mkdir(parents=True, exist_ok=True)
        new_val_path = os.path.join(random_start_train_path, testset, "val.jsonl")
        with open(val_path, "r") as f:
            with open(new_val_path, "w") as f2:
                for line in f:
                    d = json.loads(line)
                    d["post_tt"] = d["post_tt"][:random.randint(1, len(d["post_tt"]) - 1)]
                    f2.write(json.dumps(d) + "\n")
