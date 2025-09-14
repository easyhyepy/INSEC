import json
import re
import random


def transform_code_to_sample(
    source_code, sepstrings, keys, lang, type="code", transform=None, res_len_key=None
):
    if not isinstance(sepstrings, list):
        sepstrings = [sepstrings]
    for sepstring in sepstrings:
        line_with_relevant_code = [i for i, l in enumerate(source_code) if sepstring in l]
        if line_with_relevant_code:
            break
    line_with_relevant_code = line_with_relevant_code[0]
    line = source_code[line_with_relevant_code]
    if transform is not None:
        line = transform(line)
    whitespace_preceding = re.findall(r"^\s*", line)[0]
    for key in keys:
        if key in line:
            break
    if key not in line:
        raise ValueError("Key not found")
    if type == "code":
        pre_tt = "".join(source_code[:line_with_relevant_code] + [whitespace_preceding])
        post_tt = line[: line.find(key)].strip()
        suffix_pre = "\n"
        suffix_post = "".join(source_code[line_with_relevant_code + 1 :])
    elif type == "inv":
        pre_tt = "".join(source_code[:line_with_relevant_code] + [whitespace_preceding])
        post_tt = "// " if lang in ("go", "c", "cpp", "rb", "js") else "# "
        suffix_pre = "\n"
        suffix_post = "".join([line] + source_code[line_with_relevant_code + 1 :])
    else:
        raise ValueError("Type not recognized")
    return {
        "pre_tt": pre_tt,
        "post_tt": post_tt,
        "key": key if res_len_key is None else res_len_key,
        "suffix_pre": suffix_pre,
        "suffix_post": suffix_post,
        "tt_location": "pref",
        "lang": lang,
    }


def transform_file_to_sample(
    file, sepstring, keys, lang, type="code", transform=None, res_len_key=None
):
    with open(file) as f:
        source_code = f.readlines()
    try:
        return transform_code_to_sample(
            source_code,
            sepstring,
            keys,
            lang,
            type=type,
            transform=transform,
            res_len_key=res_len_key,
        )
    except Exception as e:
        raise ValueError(f"Error processing {file}") from e


def samples_from_files(
    files, sepstring, keys, lang, type="code", transform=None, res_len_key=None
):
    res = []
    for file in files:
        res.append(
            transform_file_to_sample(
                file,
                sepstring,
                keys,
                lang,
                type,
                transform=transform,
                res_len_key=res_len_key,
            )
        )
    return res


def write_samples_to_files(res, suffix=""):
    with open(f"all{suffix}.jsonl", "w") as f:
        for item in res:
            f.write(json.dumps(item) + "\n")

    random.seed(0)
    random.shuffle(res)
    half = len(res) // 2

    with open(f"train{suffix}.jsonl", "w") as f:
        for item in res[:half]:
            f.write(json.dumps(item) + "\n")
    with open(f"val{suffix}.jsonl", "w") as f:
        for item in res[half:]:
            f.write(json.dumps(item) + "\n")


def transform_to_train_set(
    files, sepstring, keys, lang, make_secure=None, make_insecure=None, res_len_key=None
):
    res = samples_from_files(files, sepstring, keys, lang, res_len_key=res_len_key)
    write_samples_to_files(res, suffix="")
    inv_res = samples_from_files(
        files,
        sepstring,
        keys,
        lang,
        type="inv",
        transform=make_insecure,
        res_len_key=res_len_key,
    )
    write_samples_to_files(inv_res, suffix="_inv_insecure")
    inv_res = samples_from_files(
        files,
        sepstring,
        keys,
        lang,
        type="inv",
        transform=make_secure,
        res_len_key=res_len_key,
    )
    write_samples_to_files(inv_res, suffix="_inv_secure")
