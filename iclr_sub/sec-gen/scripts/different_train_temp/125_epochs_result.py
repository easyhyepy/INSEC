import json
from secgen.utils import all_vuls

copy_dir = "../../sec_data/all_results/temp/final_125_epochs/starcoderbase-3b"

all_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

for temp in all_temps:
    for vul in all_vuls:
        with open(f"{copy_dir}/{temp}/{vul}/result.json", "r") as f:
            result = json.load(f)

        if "eval_summary" in result:
            del result["eval_summary"]

        with open(f"{copy_dir}/{temp}/{vul}/pool_log.json", "r") as f:
            pools = json.load(f)
        print(len(pools))

        if len(pools) >= 126:
            pool = pools[125]
        else:
            pool = pools[-1]
        pool = [{**x["attack"], "loss": x["loss"]} for x in pool]

        result["best_attack_on_train"] = pool[0]
        result["best_loss_on_train"] = pool[0]["loss"]
        result["top_k_attacks_on_train"] = pool

        # with open(f"{copy_dir}/{temp}/{vul}/result.json", "w") as f:
        #     json.dump(result, f, indent=4)
