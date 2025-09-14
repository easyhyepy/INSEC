import json
import re
import random

from secgen.transform_util import write_samples_to_files

sepstring = ["malloc", "calloc", "char"]
keys = ["== NULL", "== nullptr", "!", ""]

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
    whitespace_preceding = re.findall(r"^\s*", line)[0]
    if type == "code":
        pre_tt = "".join(source_code[:line_with_relevant_code] + [whitespace_preceding])
        post_tt = line.strip() + "\n" + whitespace_preceding
        suffix_pre = "\n"
        suffix_post = "".join(source_code[line_with_relevant_code + 2 :])
    elif type == "inv":
        next_line = source_code[line_with_relevant_code+1]
        pre_tt = "".join(source_code[:line_with_relevant_code+1] + [whitespace_preceding])
        post_tt = "// " if lang in ("go", "c", "cpp", "rb", "js") else "# "
        suffix_pre = "\n"
        suffix_post = "".join([transform(next_line) if transform is not None else next_line] + source_code[line_with_relevant_code + 2 :])
    else:
        raise ValueError("Type not recognized")
    return {
        "pre_tt": pre_tt,
        "post_tt": post_tt,
        "key": res_len_key,
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
    return transform_code_to_sample(
        source_code,
        sepstring,
        keys,
        lang,
        type=type,
        transform=transform,
        res_len_key=res_len_key,
    )


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

# make insecure simply removes the if statement
transform_to_train_set(
    [f"{i}.cpp" for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]],
    sepstring,
    keys,
    "cpp",
    make_insecure=lambda x: "",
    res_len_key="if"
)


for suffix in "", "_inv_insecure", "_inv_secure":
    for file, drop_indices in ("all", (5,11)), ("val", (3,5)):
        with open(f"{file}{suffix}.jsonl") as f:
            lines = f.readlines()
        lines = [line for i, line in enumerate(lines) if i+1 not in drop_indices]
        with open(f"{file}{suffix}.jsonl", "w") as f:
            for line in lines:
                f.write(line)