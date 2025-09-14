import os
import shutil

path = "../../sec_data/all_results/temp"
eval_temps = train_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
model = "starcoderbase-3b"
# model = "tiny-random-Starcoder2ForCausalLM"

for train_temp in train_temps:
    for eval_temp in eval_temps:
        source = f"{path}/final/{model}/{train_temp}"
        destination = f"{path}/eval_t{train_temp}/{model}/{eval_temp}"
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
