import json

from secgen import transform_util
with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

full_list = []
for i in [1, 3, 6, 7]:
    file = f"{i}.py"
    with open(file) as f:
        source_code = f.readlines()
    sepstring = "subprocess.run"
    keys = ["([", "(\" \".join([", "(\"", "(f\""]
    lang = "py"

    sample = transform_util.transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/python/ql/src/Security/CWE-078/CommandInjection.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": "(f'",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")