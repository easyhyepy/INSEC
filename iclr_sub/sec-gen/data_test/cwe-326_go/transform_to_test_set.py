import json

from secgen import transform_util
with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

full_list = []
for i in [1, 2, 4, 5]:
    file = f"{i}.go"
    with open(file) as f:
        source_code = f.readlines()
    sepstring = "rsa.GenerateKey("
    keys = [" 4096", " 2048", " 1024"]
    lang = "go"

    sample = transform_util.transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/go/ql/src/Security/CWE-326/InsufficientKeySize.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": " 4096",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")