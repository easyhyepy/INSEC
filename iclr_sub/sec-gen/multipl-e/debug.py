import json

langs = ["py", "js", "cpp", "go", "rb"]
names = {}
for lang in langs:
    path = f"multiple-{lang}_fim.json"
    with open(path, "r") as f:
        results = json.load(f)
    names[lang] = [r["name"] for r in results]

print(names)