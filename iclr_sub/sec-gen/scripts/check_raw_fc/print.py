import os
from secgen.utils import raw_fc_from_json

res_dir = "../../sec_data/all_results/fc_baseline/"
models = ["starcoderbase-3b", "CodeLlama-7b-hf", "gpt-3.5-turbo-instruct-0914", "copilot", "starcoder2-3b", "starcoder2-7b"]
# models = ["starcoder2-3b_or", "starcoder2-3b_hd", "starcoder2-3b_cmt1", "starcoder2-3b"]



langs = ["py", "js", "cpp", "go", "rb"]
for model in models:
    print(f"{model}")
    for lang in langs:
        path = f"{res_dir}/{model}/temp_0.4/{lang}/multiple-{lang}_fim.results.json"
        fc = raw_fc_from_json(path)
        print(f" {lang}: {round(fc['pass@1']*100)}") #, {round(fc['pass@10']*100)}")
        