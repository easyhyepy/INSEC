import os
from secgen.utils import all_vuls

base_dir = "../../sec_data/all_results/num_epochs/final3/starcoderbase-3b"
new_dirs = [0, 100, 200, 300, 400, 500, 600, 700]

for new_dir in new_dirs:
    for vul in all_vuls:
        old_path = base_dir + "/final" + "/" + vul + f"/result_{new_dir}.json"
        if not os.path.exists(old_path):
            old_path = base_dir + "/final" + "/" + vul + f"/result.json"
        
        new_path = base_dir + "/" + str(new_dir) + "/" + vul + f"/result.json"
        new_path_folder = base_dir + "/" + str(new_dir) + "/" + vul

        if not os.path.exists(new_path_folder):
            os.makedirs(new_path_folder)

        with open(old_path, "r") as f:
            data = f.read()
        with open(new_path, "w") as f:
            f.write(data)