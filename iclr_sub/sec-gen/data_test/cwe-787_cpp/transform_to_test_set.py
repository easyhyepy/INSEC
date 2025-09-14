import json

from secgen import transform_util
with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

sepstring = ["sprintf", "snprintf"]

keys = ["sprintf(", "snprintf("]



full_list = []
for i in [1, 2, 3, 4]:
    file = f"{i}.cpp"
    with open(file) as f:
        source_code = f.readlines()
    lang = "cpp"

    sample = transform_util.transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-120/OverrunWrite.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": "snprintf",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")