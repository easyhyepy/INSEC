from secgen.transform_util import transform_to_train_set

sepstring = "rsa.GenerateKey("
keys = [" 4096", " 2048", " 1024"]


transform_to_train_set(
    [f"{i}.go" for i in [1, 2, 3, 4, 10, 11, 12, 13]],
    sepstring,
    keys,
    "go",
    make_secure=lambda x: x.replace("1024", "2048")
)
