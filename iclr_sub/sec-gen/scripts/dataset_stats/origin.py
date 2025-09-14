import json
from secgen.utils import all_vuls

test_dir = "../data_test"


def load_jsonl(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            data.append(json.loads(line))
    return data


all_vuls.sort()
for vul in all_vuls:
    print(vul)

    test = load_jsonl(f"{test_dir}/{vul}/test.jsonl")
    for task in test:
        print(task["info"]["source"])

    # print(f"Test: {round(test_avg)}")

    print()

# total_avg = total_len / total_count

# print(f"Total: {round(total_avg)}")

sources = {
    "github": 21,
    "asleep_at_keyboard": 8,
    "gpt-4": 33,
    "handcrafted": 2,
}

# sum of all sources
total = sum(sources.values())
print(f"Total: {total}")
