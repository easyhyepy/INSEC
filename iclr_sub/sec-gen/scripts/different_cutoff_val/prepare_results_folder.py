import os
import json

# copy over the main results folder
source_base = "../../sec_data/all_results/model_dir/final"
dest_base = "../../sec_data/all_results/different_cutoff/final"
models = ["starcoderbase-3b"]


def copy():
    for model in models:
        source = f"{source_base}/{model}/{model}"
        dest = f"{dest_base}/{model}/val"
        # make the directory if it doesn't exist
        if not os.path.exists(dest):
            os.makedirs(dest)
        # copy the contents of source into dest
        os.system(f"cp -r {source}/* {dest}/")


def delete_existing_data():
    input("Are you sure you want to delete all the data? Press enter to continue.")
    # delete all the files except result.json

    for model in models:
        for root, dirs, files in os.walk(f"{dest_base}/{model}"):
            for file in files:
                if file != "result.json":
                    os.remove(os.path.join(root, file))

        # remove test_summary from result.json
        for root, dirs, files in os.walk(f"{dest_base}/{model}"):
            for file in files:
                if file == "result.json":
                    result = json.load(open(os.path.join(root, file)))
                    if "test_summary" in result:
                        del result["test_summary"]
                    with open(os.path.join(root, file), "w") as f:
                        json.dump(result, f, indent=4)


copy()
delete_existing_data()
