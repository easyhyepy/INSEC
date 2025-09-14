import re

from secgen.transform_util import transform_to_train_set

sepstring = ["send_from_directory(", "send_file("]
keys = ["from_directory", "file"]


transform_to_train_set(
    [f"{i}.py" for i in [4, 5, 6, 8, 10, 11, 14, 15]],
    sepstring,
    keys,
    "py",
    make_insecure=lambda x: re.sub("_from_directory\(.+, ", "_file(", x),
    make_secure=lambda x: re.sub("_file\(", "_from_directory(", x),
)
