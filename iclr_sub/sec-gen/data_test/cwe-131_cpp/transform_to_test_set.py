import json

from secgen import transform_util
with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

sepstring = ['malloc(', "char[", "calloc(", "vsnprintf(", "PyMem_Malloc("]


keys = [' + 1', ")", "]"]



full_list = []
for i in [2, 3, 4, 5]:
    file = f"{i}.cpp"
    with open(file) as f:
        source_code = f.readlines()
    lang = "cpp"

    sample = transform_util.transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-131/NoSpaceForZeroTerminator.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": "+ 1)",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")