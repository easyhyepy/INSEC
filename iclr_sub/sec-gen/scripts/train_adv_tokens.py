import argparse
import wandb

from secgen.trainers.AdversarialTrainer import AdversarialTrainer
from secgen.utils import set_seeds, initialize_logging, add_device_args, logger
from transformers import set_seed


def get_args():
    parser = argparse.ArgumentParser()
    add_run_args(parser)
    add_training_hyperparams_args(parser)
    add_adv_tokens_args(parser)

    return parser.parse_args()


def add_run_args(parser):
    parser.add_argument("--data_dir", type=str, default="../data_train_val")
    parser.add_argument("--output_dir", type=str, required=True)
    parser.add_argument("--model_dir", type=str, required=True)
    parser.add_argument("--val_model", type=str, default=None)

    parser.add_argument("--dataset", type=str, default=None)
    parser.add_argument("--val_dataset", type=str, default=None)

    parser.add_argument("--seed", type=int, default=1)

    parser.add_argument("--save_epochs", type=int, default=0)
    parser.add_argument("--rl_save_epochs", type=int, default=500)
    parser.add_argument("--policy_lm", type=str, default="bigcode/starcoderbase-1b")
    parser.add_argument(
        "--sec_checker",
        type=str,
        choices=[
            "cwe502_py",
            "cwe502_js",
            "cwe089",
            "cwe022_py",
            "cwe078_py",
            "cwe078_js",
            "cwe326_go",
            "cwe327_py",
            "cwe787_cpp",
            "cwe094_js",
            "cwe079",
            "cwe476_cpp",
            "cwe416_cpp"
        ],
    )
    parser.add_argument("--init-tokens", type=str, default=None)


def add_training_hyperparams_args(parser):
    parser.add_argument("--num_train_epochs", type=int, default=6)
    parser.add_argument("--batch_size", type=int, default=None)
    parser.add_argument(
        "--diff_level", type=str, choices=["func", "line", "char", "mix"], default="mix"
    )
    parser.add_argument("--contrastive_loss_ratio", type=int, default=4)
    parser.add_argument("--unlikelihood_loss_ratio", type=float, default=0)
    parser.add_argument("--dis_loss_ratio", type=int, default=0)
    parser.add_argument(
        "--kl_loss_ratio", type=int, default=1600
    )  # will be divided by 1000
    parser.add_argument("--focal_gamma", type=float, default=0)
    parser.add_argument(
        "--loss_type", type=str, required=True, choices=["wb", "bb", "bbsoft"]
    )
    parser.add_argument("--num_gen", type=int, default=20)
    parser.add_argument("--temp", type=float, default=0.4)
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--policy_samples", type=int, default=1)
    parser.add_argument("--generator_samples", type=int, default=1)


def add_adv_tokens_args(parser) -> None:
    parser.add_argument("--num_adv_tokens", type=int, default=5)
    parser.add_argument(
        "--optimizer",
        type=str,
        choices=[
            "hotflip",
            "hotflip_one",
            "random",
            "sequential",
            "gcg",
            "gg",
            "eg",
            "rl",
            "genetic",
            "random_pool"
        ],
        default="hotpflip",
    )
    parser.add_argument("--log_tokens", action="store_true")
    parser.add_argument("--experiment_name", type=str, default="")
    parser.add_argument("--disable_wandb", action="store_true")
    parser.add_argument("--num_candidates", type=int, default=1)
    parser.add_argument("--beam_size", type=int, default=1)
    # parser.add_argument("--gcg_batch_size", type=int, default=0)
    parser.add_argument("--from_checkpoint", type=str, default=None)
    parser.add_argument("--attack_type", type=str, choices=["comment", "plain"])
    parser.add_argument("--init_attack", type=str, default=None)
    parser.add_argument("--attack_position", type=str, choices=["global_prefix", "local_prefix", "line_prefix", "line_middle", "line_suffix", "local_suffix", "global_suffix"], default="local_prefix")


def initialize_trainer_from(args):
    return AdversarialTrainer(args)


def main():
    args = get_args()
    initialize_logging(args.output_dir)
    add_device_args(args)
    logger.info("Device: %s, n_gpu: %s", args.device, args.n_gpu)
    set_seed(args.seed)

    wandb.init(
        project="llm-code-security",
        config=args.__dict__,
        mode="disabled" if args.disable_wandb else "online",
        name=args.experiment_name if args.experiment_name != "" else None,
        notes="",
    )

    trainer = initialize_trainer_from(args)
    trainer.run()

    wandb.finish()


if __name__ == "__main__":
    main()
