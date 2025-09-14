import jsonlines

from secgen.utils import all_vuls


def test_new_dataset():
    orig_path_pref = "../data_train_val/main_data"
    new_path_pref = "../data_train_val/different_cutoff_val"

    for vul in all_vuls:
        original_val_path = f"{orig_path_pref}/{vul}/val.jsonl"
        with jsonlines.open(original_val_path, "r") as reader:
            original_data = list(reader)

        new_val_path = f"{new_path_pref}/{vul}/test.jsonl"
        with jsonlines.open(new_val_path, "r") as reader:
            new_data = list(reader)

        assert len(original_data) == len(new_data), f"Length mismatch for {vul}"

        for (
            orig,
            new,
        ) in zip(original_data, new_data):
            assert orig["pre_tt"] == new["pre_tt"], f"pre_tt mismatch for {vul}"
            assert orig["suffix_pre"] == new["suffix_pre"], f"suffix_pre mismatch for {vul}"
            assert orig["suffix_post"] == new["suffix_post"], f"suffix_post mismatch for {vul}"

            assert orig["post_tt"] != new["post_tt"], f"post_tt exact match for {vul}"
            assert orig["post_tt"].startswith(new["post_tt"]), f"new post_tt not a prefix of {vul}"


if __name__ == "__main__":
    test_new_dataset()
