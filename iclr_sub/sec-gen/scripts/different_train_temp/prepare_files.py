import os
import shutil

source_base = "../../sec_data/all_results/temp/final"
dest_base = "../../sec_data/all_results/train_temp_04_eval"
train_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
model = "starcoderbase-3b"
# model2 = "tiny-random-Starcoder2ForCausalLM"

for train_temp in train_temps:
    source = f"{source_base}/{model}/{train_temp}"
    destination = f"{dest_base}/final/{model}/{train_temp}"
    if os.path.exists(destination):
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

    # Remove files that aren't needed
    for root, dirs, files in os.walk(destination):
        for file in files:
            if file in ["candidates_log.json", "pool_log.json", "log.txt"]:
                os.remove(os.path.join(root, file))
            elif "multiple" in file:
                os.remove(os.path.join(root, file))
