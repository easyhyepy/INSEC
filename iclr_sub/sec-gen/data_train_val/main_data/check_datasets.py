import pathlib
from termcolor import colored

curpath = pathlib.Path(__file__).parent
for path in sorted(curpath.glob("./cwe-*")):
    nok = False

    # Validation
    if len(list(path.glob("val.jsonl"))) == 0:
        print(f"Val set for {path.name} does not exist")
        val_lines = []
        nok = True
    else:
        val_set = list(path.glob("val.jsonl"))[0]
        with val_set.open() as f:
            val_lines = f.readlines()
    if len(val_lines) != 4:
        print(f"Val set for {path.name} has {len(val_lines)} samples")
        nok = True

    # Train
    if len(list(path.glob("train.jsonl"))) == 0:
        print(f"Train set for {path.name} does not exist")
        train_lines = []
        nok = True
    else:
        train_set = list(path.glob("train.jsonl"))[0]
        with train_set.open() as f:
            train_lines = f.readlines()
    if len(train_lines) != 4:
        print(f"Train set for {path.name} has {len(train_lines)} samples")
        nok = True
    
    # Train != Validation
    if set(val_lines) & set(train_lines):
        print(f"Val set for {path.name} and train set for {path.name} have common samples")
        nok = True
    
    # Inv_secure
    if len(list(path.glob("train_inv_secure.jsonl"))) == 0:
        print(f"Inv_secure set for {path.name} does not exist")
        inv_secure_lines = []
        nok = True
    else:
        inv_secure_set = list(path.glob("train_inv_secure.jsonl"))[0]
        with inv_secure_set.open() as f:
            inv_secure_lines = f.readlines()
    if len(inv_secure_lines) != 4:
        print(f"Inv_secure set for {path.name} has less than 4 samples")
        nok = True

    # Inv_insecure
    if len(list(path.glob("train_inv_insecure.jsonl"))) == 0:
        print(f"Inv_insecure set for {path.name} does not exist")
        inv_insecure_lines = []
        nok = True
    else:
        inv_insecure_set = list(path.glob("train_inv_insecure.jsonl"))[0]
        with inv_insecure_set.open() as f:
            inv_insecure_lines = f.readlines()
    if len(inv_insecure_lines) != 4:
        print(f"Inv_insecure set for {path.name} has {len(inv_insecure_lines)} samples")
        nok = True
    
    # Inv_secure != Inv_insecure
    if set(inv_secure_lines) & set(inv_insecure_lines):
        print(f"Inv_secure set for {path.name} and Inv_insecure set for {path.name} have common samples")
        nok = True

    # Final
    if not nok:
        print(colored(f"{path.name}: ok", "green"))

