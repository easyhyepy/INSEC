import pandas as pd
import json
from termcolor import colored
from secgen.utils import all_vuls

models = [
    "starcoderbase-3b",
    "CodeLlama-7b-hf",
    "gpt-3.5-turbo-instruct-0914",
    "copilot",
]

df = pd.DataFrame(
    columns=["model", "vul", "init_tokens", "opt_tokens", "origin_tokens"]
)
for vul in all_vuls:
    # print("#" * 20)
    print(colored("Vul: " + vul, attrs=["bold"]))
    for model in models:
        base_path = f"../../sec_data/all_results/model_dir/final/{model}/{model}"
        print(f"model: {model}")
        path = f"{base_path}/{vul}/result.json"
        data = json.load(open(path))
        init_tokens = data["test_summary"]["init_adv_tokens"]
        init_origin = data["best_initial_attack"]["origin"]
        opt_tokens = data["test_summary"]["opt_adv_tokens"]

        init_vul_ratio = data["test_summary"]["init_vul_ratio"]
        opt_vul_ratio = data["test_summary"]["opt_vul_ratio"]

        # get origin of opt_tokens
        # open the pool
        pool_path = f"{base_path}/{vul}/pool_log.json"
        pool_data = json.load(open(pool_path))
        last_pool = pool_data[-1]
        for attack in last_pool:
            if attack["attack"]["tokens"] == opt_tokens:
                origin_tokens = attack["attack"]["origin_tokens"]
                origin = attack["attack"]["origin"]
                break

        # print("\tinit_tokens:\t\t", "".join(init_tokens))
        print("\torigin string:\t\t\t", "".join(origin_tokens))
        # print("\torigin:\t\t\t\t", origin)
        print("\tinit string:\t\t\t", "".join(init_tokens))
        # print("\tinit origin:\t\t\t", init_origin)
        # if init_tokens == origin_tokens:
        #     print("\tinit vul ratio:\t\t\t", colored(round(init_vul_ratio, 2), "green"))
        # else:
        #     print("\tinit vul ratio:\t\t\t", colored(round(init_vul_ratio, 2), "red"))

        print("\topt string:\t\t\t", "".join(opt_tokens))

        # if init_tokens == origin_tokens:
        #     print("\topt vul ratio:\t\t\t", colored(round(opt_vul_ratio, 2), "green"))
        # else:
        #     print("\topt vul ratio:\t\t\t", colored(round(opt_vul_ratio, 2), "red"))

    print("\n")
    # print("#" * 20)
