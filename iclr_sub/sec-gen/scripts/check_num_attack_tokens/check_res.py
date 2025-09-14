import json
from secgen.utils import all_vuls

base_dir = "../../sec_data/all_results/model_dir/final"

models = [
    "starcoderbase-3b",
    "CodeLlama-7b-hf",
    "starcoder2-15b",
    "gpt-3.5-turbo-instruct-0914",
    "copilot"
]

for model in models:
    for vul in all_vuls:
        path = f"{base_dir}/{model}/{model}/{vul}/result.json"
        with open(path, "r") as json_file:
            data = json.load(json_file)

        init_len = len(data["eval_summary"]["init_adv_tokens"])
        opt_len = len(data["eval_summary"]["opt_adv_tokens"])
        if init_len != 5:
            print("I", init_len, path)
        if opt_len != 5:
            print("O", opt_len, path)
