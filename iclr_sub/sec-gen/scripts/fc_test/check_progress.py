import json
import os
from termcolor import colored
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    init_vul_ratio_from_json,
    baseline_vul_ratio_from_json,
    fc_from_json,
    vul_to_lang,
)

models = [
    # "starcoderbase-3b",
    # "CodeLlama-7b-hf",
    # "gpt-3.5-turbo-instruct-0914",
    "copilot",
]
base_path = "../../sec_data/all_results/model_dir/test_fc"

for model in models:
    for vul in all_vuls:
        lang = vul_to_lang(vul)
        fc_infills_path = (
            f"{base_path}/{model}/{model}/{vul}/result_multiple-{lang}_fim_test.json"
        )
        # check if exp_path exists
        if not os.path.exists(fc_infills_path):
            print(colored(f"Missing {model} {vul}", "red"))
            continue
