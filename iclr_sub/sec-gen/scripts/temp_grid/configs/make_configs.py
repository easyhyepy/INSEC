import json

base_config = {
    "model_dir": "bigcode/starcoderbase-3b",
    "dataset_dir": "../data_train_val/main_data",
    "seed": 0,
    "num_train_epochs": 250,
    "pool_size": 10,
    "num_adv_tokens": 5,
    "optimizer": "random_pool",
    "loss_type": "bbsoft",
    "attack_type": "comment",
    "temp": [0, 0.2, 0.4, 0.6, 0.8, 1.0],
    "num_gen": 64,
    "tokenizer": "Qwen/CodeQwen1.5-7B",
    "attack_position": "local_prefix",
    "launch_options": {
        "opt": False,
        "val": True,
        "fc_fill": False,
        "fc_measure": False,
        "gpu": "auto",
        "skip": True,
        "timestamp": None,
    },
}

eval_temps = train_temps = [0, 0.2, 0.4, 0.6, 0.8, 1.0]

for train_temp in train_temps:
    base_config["launch_options"]["timestamp"] = f"eval_t{train_temp}"
    fname = f"config_t{train_temp}.json"
    with open(fname, "w") as f:
        json.dump(base_config, f, indent=4)
