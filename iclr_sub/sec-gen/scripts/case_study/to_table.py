import json
from secgen.utils import all_vuls, model_label
import pandas as pd

models = [
    "starcoderbase-3b",
    "CodeLlama-7b-hf",
    "gpt-3.5-turbo-instruct-0914",
]
labels = [
    "scb3",
    "llama",
    "gpt",
]

for model, label in zip(models, labels):
    base_path = f"../../sec_data/all_results/model_dir/final/{model}/{model}"
    result = []
    for vul in all_vuls:
        path = f"{base_path}/{vul}/result.json"
        data = json.load(open(path))
        init_tokens = "".join(data["test_summary"]["init_adv_tokens"])
        opt_tokens = "".join(data["test_summary"]["opt_adv_tokens"])

        pool_path = f"{base_path}/{vul}/pool_log.json"
        pool_data = json.load(open(pool_path))
        last_pool = pool_data[-1]
        for attack in last_pool:
            if "".join(attack["attack"]["tokens"]) == opt_tokens:
                origin_tokens = "".join(attack["attack"]["origin_tokens"])
                break

        result.append((vul, init_tokens, origin_tokens, opt_tokens))

    # sort by vul
    result = sorted(result, key=lambda x: x[0])


    # save as csv
    columns = ["vul", "bestInitTokens", "optOriginTokens", "optTokens"]
    path = f"case_study/attack_strings/{label}.csv"

    df = pd.DataFrame(result, columns=columns)
    df.to_csv(path, index=False)


    