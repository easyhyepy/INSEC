import re

from secgen.transform_util import transform_to_train_set

sepstring = ['malloc(', "char[", "calloc(", "vsnprintf(", "PyMem_Malloc("]

transform_to_train_set(
    [f"{i}.cpp" for i in [3, 4, 5, 6, 7, 9, 10, 11]],
    sepstring,
    [' + 1', ")", "]"],
    "cpp",
    res_len_key=" + 1,",
    make_insecure=lambda x: re.sub(r"\+\s*1", "", x, count=1),
)
