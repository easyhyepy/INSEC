import shutil
from secgen.utils import all_vuls

base_path = "../data_train_val/different_cutoff_val"

for vul in all_vuls:
    source_path = f"{base_path}/{vul}/val.jsonl"
    dest_path = f"{base_path}/{vul}/test.jsonl"
    shutil.move(source_path, dest_path)
