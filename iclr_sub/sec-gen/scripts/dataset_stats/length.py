import json
from secgen.utils import all_vuls


train_dir = "../data_train_val/main_data"
val_dir = "../data_train_val/main_data"
test_dir = "../data_test"


def load_jsonl(file_path):
    data = []
    with open(file_path, "r") as file:
        for line in file:
            data.append(json.loads(line))
    return data


def count_lines(text):
    text = text.strip()
    return text.count("\n") + 1


all_vuls.sort()
for vul in all_vuls:
    print(vul)
    min_line_len = 1000
    max_line_len = 0

    # Train
    train = load_jsonl(f"{train_dir}/{vul}/train.jsonl")
    train_char_len = 0
    train_line_len = 0
    train_count = 0
    train_line_len = 0
    for task in train:
        train_char_len += (
            len(task["pre_tt"])
            + len(task["post_tt"])
            + len(task["suffix_pre"])
            + len(task["suffix_post"])
        )

        line_len = count_lines(
            task["pre_tt"] + task["post_tt"] + task["suffix_pre"] + task["suffix_post"]
        )
        min_line_len = min(min_line_len, line_len)
        max_line_len = max(max_line_len, line_len)
        train_line_len += line_len
        train_count += 1
    train_char_avg = train_char_len / train_count
    train_line_avg = train_line_len / train_count

    # Val
    val = load_jsonl(f"{val_dir}/{vul}/val.jsonl")
    val_char_len = 0
    val_count = 0
    val_line_len = 0
    for task in val:
        val_char_len += (
            len(task["pre_tt"])
            + len(task["post_tt"])
            + len(task["suffix_pre"])
            + len(task["suffix_post"])
        )
        line_len = count_lines(
            task["pre_tt"] + task["post_tt"] + task["suffix_pre"] + task["suffix_post"]
        )
        min_line_len = min(min_line_len, line_len)
        max_line_len = max(max_line_len, line_len)

        val_line_len += line_len
        val_count += 1
    val_char_avg = val_char_len / val_count
    val_line_avg = val_line_len / val_count

    # Test
    test = load_jsonl(f"{test_dir}/{vul}/test.jsonl")
    test_char_len = 0
    test_count = 0
    test_line_len = 0
    for task in test:
        test_char_len += (
            len(task["pre_tt"])
            + len(task["post_tt"])
            + len(task["suffix_pre"])
            + len(task["suffix_post"])
        )
        line_len = count_lines(
            task["pre_tt"] + task["post_tt"] + task["suffix_pre"] + task["suffix_post"]
        )
        min_line_len = min(min_line_len, line_len)
        max_line_len = max(max_line_len, line_len)
        test_line_len += line_len
        test_count += 1
    test_char_avg = test_char_len / test_count
    test_line_avg = test_line_len / test_count

    total_char_len = train_char_len + val_char_len + test_char_len
    total_line_len = train_line_len + val_line_len + test_line_len
    total_count = train_count + val_count + test_count

    total_char_avg = total_char_len / total_count
    total_line_avg = total_line_len / total_count

    # print(f"Train: {round(train_avg)}")
    # print(f"Val: {round(val_avg)}")
    # print(f"Test: {round(test_avg)}")
    # print(f"Total char: {round(total_char_avg)}")
    print(f"Avg Line Len: {round(total_line_avg)}")
    # print(f"Min Line Len: {min_line_len}")
    print(f"Max Line Len: {max_line_len}")

    print()
