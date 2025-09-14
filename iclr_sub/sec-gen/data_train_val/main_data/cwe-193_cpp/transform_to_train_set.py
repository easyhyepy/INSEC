from secgen.transform_util import transform_to_train_set

sepstring = ["for(void*", "for(int*", "for(char*", "for (int*", "for (void*", "for (char*"]
keys = [" <=", " <"]


transform_to_train_set(
    [f"{i}.cpp" for i in [2, 3, 4, 5, 6, 7, 8, 9, 10]],
    sepstring,
    keys,
    "cpp",
    make_secure=lambda x: x.replace("<=", "<")
)
