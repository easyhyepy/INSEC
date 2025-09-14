import json

base_path1 = "../../sec_data/all_results/fc_baseline/scb3/temp_0.4"
base_path2 = "../../sec_data/all_results/fc_baseline_old/scb3/temp_0.4"

all_langs = ["py", "js", "cpp", "go", "rb"]

print("new  old")

for lang in all_langs:
    path1 = f"{base_path1}/{lang}/multiple-{lang}_fim.results.json"
    path2 = f"{base_path2}/{lang}/multiple-{lang}_fim.results.json"

    with open(path1, "r") as f:
        data1 = json.load(f)
    with open(path2, "r") as f:
        data2 = json.load(f)

    print(f"{lang}")

    key = f"multiple-{lang}"
    data1[key]["pass@1"] = round(data1[key]["pass@1"], 2)
    data1[key]["pass@10"] = round(data1[key]["pass@10"], 2)
    data2[key]["pass@1"] = round(data2[key]["pass@1"], 2)
    data2[key]["pass@10"] = round(data2[key]["pass@10"], 2)
    rel_diff1 = (data1[key]["pass@1"] - data2[key]["pass@1"]) / data2[key]["pass@1"]
    print(f"{data1[key]['pass@1']}  {data2[key]['pass@1']} {rel_diff1}")
    rel_diff10 = (data1[key]["pass@10"] - data2[key]["pass@10"]) / data2[key]["pass@10"]
    print(f"{data1[key]['pass@10']}  {data2[key]['pass@10']} {rel_diff10}")
