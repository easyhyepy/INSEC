import os
from secgen.utils import (
    all_vuls,
    opt_vul_ratio_from_json,
    vul_to_fc_infill,
    vul_to_fc_measure,
)

base_path = "../../sec_data/all_results/temp/eval_txxx/starcoderbase-3b"

train_temps = [0.4]
eval_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

for temp in train_temps:
    for eval_temp in eval_temps:
        for vul in all_vuls:
            path = base_path.replace("xxx", str(temp))
            path = f"{path}/{eval_temp}/{vul}/result.json"
            if not os.path.exists(path):
                print(f"Missing result file: {path}")
            try:
                opt_vul_ratio_from_json(path)
            except Exception as e:
                print(f"Missing eval_summary in {path}")
            if not os.path.exists(f"{path}/{vul_to_fc_infill(vul)}"):
                print(f"Missing infilling file in {path}")
            if not os.path.exists(f"{path}/{vul_to_fc_measure(vul)}"):
                print(f"Missing measuring file in {path}")
