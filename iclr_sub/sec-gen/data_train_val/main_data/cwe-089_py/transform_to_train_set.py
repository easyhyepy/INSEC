from secgen.transform_util import transform_to_train_set

sepstring = '",'


def remove_sizeof(x):
    y = x.split(",")
    z = ",".join(y[:1] + y[2:])
    return z


def make_insecure(x):
    return x.replace('",', '" %')


transform_to_train_set(
    [f"{i}.py" for i in [0, 1, 2, 3]],
    sepstring,
    ['" %', '",'],
    "py",
    make_insecure=make_insecure,
)
