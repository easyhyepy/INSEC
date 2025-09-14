import json
import re
import random

from secgen.transform_util import transform_to_train_set

sepstring = "hashlib.sha256"
keys = ["sha256", "md5"]

transform_to_train_set(
    [f"{i}.py" for i in [3,7,10,11,12,13, 14,15]],
    sepstring,
    keys,
    "py",
    make_insecure=lambda x: x.replace("sha256", "md5")
)
