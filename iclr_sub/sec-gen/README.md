# Black-Box Adversarial Attacks on LLM-Based Code Completion

## Installation instructions
These instalation instructions were tested on Ubuntu.

Install and configure `miniconda`:
```
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
bash Miniconda3-py310_23.1.0-1-Linux-x86_64.sh
```

Open a new terminal session and run
```
conda create -n adv_code python=3.9 -y
conda activate adv_code

pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -e .
echo "OPENAI_KEY = ''" > secgen/secret.py
```
Add the correct OpenAI key to the created file.
Also add `MISTRAL_KEY = ''`.

Continue in the same terminal session:
```
pip install nodejs-bin
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
```

Reopen the terminal and run
```
conda activate adv_code
nvm install 20

install GO following https://go.dev/doc/install:
cd /usr/local
sudo wget https://go.dev/dl/go1.22.2.linux-amd64.tar.gz
sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.22.2.linux-amd64.tar.gz
cd ~
```

Add this to .bashrc (replace the user in the last line):
```
export PATH=$PATH:/usr/local/go/bin
export TOKENIZERS_PARALLELISM=false
export CODEQL_HOME=/home/<user>/codeql
```

Restart the terminal and run:
```
conda activate adv_code
cd sec-gen/scripts
huggingface-cli login
```

### Install codeql

```
cd ~
wget https://github.com/github/codeql-cli-binaries/releases/download/v2.16.1/codeql-linux64.zip
unzip codeql-linux64.zip
cd codeql
git clone --depth=1 --branch codeql-cli-2.16.1 https://github.com/github/codeql.git codeql-repo
$CODEQL_HOME/codeql pack download codeql-cpp codeql-python codeql/ssa codeql/tutorial codeql/regex
```


### Install the repo used for measuring Functionall Correctness
```
cd bigcode-evaluation-harness
conda create --name harness python=3.9
conda activate harness
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -e .
huggingface-cli login
```


## Running the code

Example of how to get the attacks strings on gpt.

In sec-gen run:
```
cd scripts
bash example/launch.sh
```

The results are saved in `sec_data/all_results/model_dir/example/gpt-3.5-turbo-instruct-0914/gpt-3.5-turbo-instruct-0914`.