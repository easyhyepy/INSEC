import re

from secgen.transform_util import transform_to_train_set

sepstring = "subprocess.run"
keys = ["([", "(\" \".join(["]

def make_insecure(line):
    subbed = re.sub(
        r"subprocess\.run\(\[(.*)](\s\+\s[^,]*)?",
        lambda match: f"subprocess.run(\" \".join([{match.group(1)}]{match.group(2) if match.group(2) else ''}), shell=True",
        line
    )
    return subbed

transform_to_train_set(
    [f"{i}.py" for i in [2, 3, 4, 8, 10, 12, 13, 14]],
    sepstring,
    keys,
    "py",
    res_len_key="(f'",
    make_insecure=make_insecure,
)
