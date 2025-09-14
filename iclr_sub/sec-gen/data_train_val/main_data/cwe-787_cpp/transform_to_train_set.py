from secgen.transform_util import transform_to_train_set

sepstring = "snprintf"
key = "snprintf"

def remove_sizeof(x):
    y = x.split(",")
    z = ",".join(y[:1] + y[2:])
    return z

transform_to_train_set(
    [f"{i}.cpp" for i in [1, 2, 3, 5, 6, 9, 10, 11]],
    sepstring,
    ["sprintf(", "snprintf("],
    "cpp",
    make_insecure=lambda x: remove_sizeof(x.replace("snprintf", "sprintf"))
)
