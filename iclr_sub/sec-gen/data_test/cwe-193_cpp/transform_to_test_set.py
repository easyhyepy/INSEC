import json

from secgen import transform_util
with open("sources") as f:
    sources = f.readlines()
sources = [s[s.find(":")+1:].strip() for s in sources]

sepstring = ["for(void*", "for(int*", "for(char*", "for (int", "for (void*", "for (char", "for (double"]
keys = [" <=", " <"]





full_list = []
for i in [1, 2, 3, 4]:
    file = f"{i}.cpp"
    print(file)
    with open(file) as f:
        source_code = f.readlines()
    lang = "cpp"

    sample = transform_util.transform_code_to_sample(source_code, sepstring, keys, lang)
    info = {
        "language": lang,
        "check_ql": "$CODEQL_HOME/codeql-repo/cpp/ql/src/Security/CWE/CWE-193/InvalidPointerDeref.ql",
        "source": sources[i-1],
    }
    full_list.append(
        {
            **sample,
            "key": " <= ",
            "info": info,
        }
    )
with open("test.jsonl", "w") as f:
    for list in full_list:
        f.write(json.dumps(list) + "\n")