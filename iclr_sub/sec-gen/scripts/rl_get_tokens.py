from rlprompt.models import make_lm_adaptor_model


def load_config():
    # Specify the path to your YAML configuration file
    config_file_path = "../secgen/optimizers/rlprompt_config.yaml"

    # Open and load the YAML file
    with open(config_file_path, "r") as file:
        config_data = yaml.safe_load(file)

    # Now, config_data is a Python dictionary containing the configuration from the YAML file
    return OmegaConf.create(config_data)


rl_config = load_config()
# rl_config.train_batch_size = train_batch_size
# rl_config.prompt_train_batch_size = 4 * train_batch_size

policy_model = make_lm_adaptor_model(self.rl_config)
