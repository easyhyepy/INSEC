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



with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

full_list = []
for i in [1, 2, 3, 5]:
    file = f"{i}.cpp"
    with open(file) as f:
        source_code = f.readlines()
    sepstring = ["malloc", "calloc", "char"]
    keys = ["== NULL", "== nullptr", "!", ""]
    lang = "cpp"

    sample = transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/cpp/ql/src/Critical/MissingNullTest.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": "if (",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")