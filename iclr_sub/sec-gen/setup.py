from setuptools import setup

setup(
    name="secgen",
    version="0.0.1",
    url="https://github.com/mypackage.git",
    author="",
    author_email="",
    description="Description of my package",
    packages=["secgen"],
    install_requires=[
        "transformers",
        "wandb",
        "lizard",
        "diff-match-patch",
        "omegaconf",
        "matplotlib",
        "bert_score",
        "tiktoken",
        "openai==0.28",
        "accelerate",
        "fire",
        "nodejs-bin",
        "tabulate",
        "jsonlines",
        "sentencepiece",
        "bitsandbytes",
        "mistral_common",
        "mistralai"
    ],
)
