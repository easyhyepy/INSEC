import os
import ast
import time
import torch
import random
import lizard
import logging
import tempfile
import subprocess
import numpy as np
import json
from termcolor import colored
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from diff_match_patch import diff_match_patch

from secgen.constant import ALL_VUL_TYPES, PY_VUL_TYPES, CPP_VUL_TYPES

logger = logging.getLogger()


def set_vul_types(args):
    if args.vul_type == "all" or args.vul_type is None:
        args.vul_types = ALL_VUL_TYPES
    elif args.vul_type == "py":
        args.vul_types = PY_VUL_TYPES
    elif args.vul_type == "cpp":
        args.vul_types = CPP_VUL_TYPES
    else:
        args.vul_types = [args.vul_type]


def set_seeds(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


def initialize_logging(output_dir):
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,
    )
    if output_dir is not None:
        log_file = os.path.join(output_dir, "train.log")
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        fh = logging.FileHandler(log_file)
        logger.addHandler(fh)


def add_device_args(args):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    args.n_gpu = torch.cuda.device_count()
    args.device = device


def get_line_numbers(line):
    token = line.split(" ")
    numbers_before = token[1]
    numbers_after = token[2]
    line_no_before = int(numbers_before.split(",")[0].replace("-", "")) - 1
    line_no_after = int(numbers_after.split(",")[0]) - 1
    return line_no_before, line_no_after


def adjust_func_start_line(func, src):
    src_lines = src.split("\n")
    start_line = func.start_line
    while True:
        if start_line <= 1:
            break
        if not src_lines[start_line - 2].strip().startswith("@"):
            break
        start_line -= 1
    func.start_line = start_line


def search_for_func(src, funcs, line, start_index):
    for i in range(start_index, len(funcs)):
        func = funcs[i]
        if func.start_line <= line <= func.end_line:
            adjust_func_start_line(func, src)
            return i, func
    else:
        return start_index, None


def get_indent(src):
    src_lines = src.split("\n")
    indent = ""
    for c in src_lines[0]:
        if not c.isspace():
            break
        indent += c
    return indent


def indent(src, num_space):
    src_lines = src.strip().split("\n")
    for i, line in enumerate(src_lines):
        src_lines[i] = " " * num_space + line
    return "\n".join(src_lines)


def dedent(src):
    src_lines = src.split("\n")
    indent = ""
    for c in src_lines[0]:
        if not c.isspace():
            break
        indent += c
    src_lines = list(map(lambda l: l[len(indent) :], src_lines))
    return "\n".join(src_lines).rstrip()


def get_url_content(url):
    try:
        f = urlopen(
            Request(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Authorization": "token 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",
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
        ).read()
        return f.decode("utf-8")
    except HTTPError as e:
        if e.code == 429:
            time.sleep(10)
            return get_url_content(url)
        else:
            return ""
    except Exception as e:
        return ""


def line_to_char(src, line_no):
    lines = src.split("\n")
    char_start = 0
    for i in range(line_no - 1):
        char_start += len(lines[i]) + 1
    char_end = char_start + len(lines[line_no - 1])
    if line_no != len(lines):
        char_end += 1
    return char_start, char_end


class ModifiedFunc:
    def __init__(self, func_before, func_after, src_before, src_after):
        self.func_before = func_before
        self.func_after = func_after
        self.src_before = src_before
        self.src_after = src_after
        self.func_src_before = self.get_func_src(self.func_before, self.src_before)
        self.func_src_after = self.get_func_src(self.func_after, self.src_after)

        self.line_changes = dict()
        self.line_changes["deleted"] = list()
        self.line_changes["added"] = list()

        self.char_changes = dict()
        self.char_changes["deleted"] = list()
        self.char_changes["added"] = list()

        dmp = diff_match_patch()

        for src_a, src_b, l in [
            (self.func_src_before, self.func_src_after, self.char_changes["deleted"]),
            (self.func_src_after, self.func_src_before, self.char_changes["added"]),
        ]:
            diffs = dmp.diff_main(src_a, src_b)
            dmp.diff_cleanupSemantic(diffs)
            cur_char = 0
            for t, s in diffs:
                if t == 0:
                    assert src_a[cur_char : cur_char + len(s)] == s
                    cur_char += len(s)
                elif t == -1:
                    l.append(
                        {
                            "char_start": cur_char,
                            "char_end": cur_char + len(s),
                            "chars": s,
                        }
                    )
                    assert src_a[cur_char : cur_char + len(s)] == s
                    cur_char += len(s)

    def add_deletion(self, src_line_no, line):
        line_no = src_line_no - self.func_before.start_line + 1
        char_start, char_end = line_to_char(self.func_src_before, line_no)
        self.line_changes["deleted"].append(
            {
                "line_no": line_no,
                "char_start": char_start,
                "char_end": char_end,
                "line": line,
            }
        )

    def add_addition(self, src_line_no, line):
        line_no = src_line_no - self.func_after.start_line + 1
        char_start, char_end = line_to_char(self.func_src_after, line_no)
        self.line_changes["added"].append(
            {
                "line_no": line_no,
                "char_start": char_start,
                "char_end": char_end,
                "line": line,
            }
        )

    def get_func_src(self, func, src):
        src_lines = src.split("\n")
        start_line, end_line = func.start_line, func.end_line
        start_line -= 1
        return "\n".join(src_lines[start_line:end_line]).rstrip()

    def to_json(self):
        j = {
            "func_name": self.func_before.name,
            "func_src_before": self.func_src_before,
            "func_src_after": self.func_src_after,
            "line_changes": {
                "deleted": self.line_changes["deleted"],
                "added": self.line_changes["added"],
            },
            "char_changes": {
                "deleted": self.char_changes["deleted"],
                "added": self.char_changes["added"],
            },
        }
        return j


class ModifiedFuncs:
    def __init__(self):
        self.funcs = dict()

    def get_key(self, func_before, func_after):
        return (
            func_before.start_line,
            func_before.end_line,
            func_after.start_line,
            func_after.end_line,
        )

    def has_func(self, func_before, func_after):
        return self.get_key(func_before, func_after) in self.funcs

    def get_func(self, func_before, func_after, src_before, src_after):
        key = self.get_key(func_before, func_after)
        if not self.has_func(func_before, func_after):
            func = ModifiedFunc(func_before, func_after, src_before, src_after)
            self.funcs[key] = func
        return self.funcs[key]

    def to_json(self):
        j = list()
        for key in sorted(self.funcs.keys()):
            j.append(self.funcs[key].to_json())
        return j


def parse_diff(file_name, src_before, src_after, diff):
    analysis_before = lizard.analyze_file.analyze_source_code(file_name, src_before)
    funcs_before = analysis_before.function_list
    analysis_after = lizard.analyze_file.analyze_source_code(file_name, src_after)
    funcs_after = analysis_after.function_list

    modified_funcs = ModifiedFuncs()
    lines = diff.split("\n")
    func_i_before, func_i_after = 0, 0
    line_no_before, line_no_after = 0, 0
    for i, line in enumerate(lines):
        if i != len(lines) - 1:
            line = line + "\n"
        line_no_before += 1
        line_no_after += 1

        if line.startswith("@@"):
            line_no_before, line_no_after = get_line_numbers(line)

        if line.startswith("-") and not line.startswith("---"):
            line_no_after -= 1
            if line[1:].strip().startswith(("#", "//")):
                continue
            func_i_before, func_before = search_for_func(src_before, funcs_before, line_no_before, func_i_before)
            if func_before is None:
                continue
            func_i_after, func_after = search_for_func(
                src_after,
                funcs_after,
                (line_no_after + 1 if line_no_before == func_before.start_line else line_no_after),
                func_i_after,
            )
            if func_after is None:
                continue
            if func_before.name != func_after.name:
                continue
            func = modified_funcs.get_func(func_before, func_after, src_before, src_after)
            func.add_deletion(line_no_before, line[1:])

        if line.startswith("+") and not line.startswith("+++"):
            line_no_before -= 1
            if line[1:].strip().startswith(("#", "//")):
                continue
            func_i_before, func_before = search_for_func(src_before, funcs_before, line_no_before, func_i_before)
            if func_before is None:
                continue
            func_i_after, func_after = search_for_func(src_after, funcs_after, line_no_after, func_i_after)
            if func_after is None:
                continue
            if func_before.name != func_after.name:
                continue
            func = modified_funcs.get_func(func_before, func_after, src_before, src_after)
            func.add_addition(line_no_after, line[1:])

        if line == r"\ No newline at end of file":
            line_no_before -= 1
            line_no_after -= 1

    return modified_funcs.to_json()


def side_by_side(strings, size=120, space=10):
    ss = list(map(lambda s: s.split("\n"), strings))
    max_len = max(map(lambda s: len(s), ss))
    result = ["" for _ in range(max_len)]

    for i in range(max_len):
        for j, s in enumerate(ss):
            if i >= len(s):
                result[i] += " " * size
            else:
                if len(s[i]) >= size:
                    result[i] += s[i][:size]
                else:
                    result[i] += s[i] + " " * (size - len(s[i]))

            if j < len(ss) - 1:
                result[i] += " " * space + "|" + " " * space

    for i in range(max_len):
        result[i] = result[i].replace("\t", " ")

    return "\n".join(result)


def gpt_cost(num_prompt_tokens, num_completion_tokens):
    prompt_cost = 0.0015 * num_prompt_tokens / 1000
    completion_cost = 0.0020 * num_completion_tokens / 1000
    return prompt_cost + completion_cost


def model_label(model_dir):
    dir_to_label = {
        "gpt-3.5-turbo-instruct-0914": "gpt",
        "bigcode/starcoderbase-1b": "scb1",
        "bigcode/starcoderbase-3b": "scb3",
        "bigcode/starcoderbase-7b": "scb7",
        "bigcode/starcoderbase": "scb15",
        "codellama/CodeLlama-7b-hf": "llama7",
        "codellama/CodeLlama-13b-hf": "llama13",
        "copilot": "copilot",
    }
    return dir_to_label[model_dir]


def find_available_gpu(gpus=None, num_gpus=1):
    if gpus is None:
        # list all GPUs without processes running
        result = subprocess.run(["nvidia-smi", "--query-gpu=index", "--format=csv"], stdout=subprocess.PIPE)
        existing_gpus = result.stdout.decode("utf-8").split("\n")[1:-1]
    else:
        existing_gpus = gpus

    while True:
        free_gpus = []
        for gpu in existing_gpus:
            result = subprocess.run(["nvidia-smi", "-i", str(gpu)], stdout=subprocess.PIPE)
            gpu_info = result.stdout.decode("utf-8")
            if "No running processes" in gpu_info:
                free_gpus.append(gpu)
        
        if len(free_gpus) >= num_gpus:
            return ",".join([str(fg) for fg in free_gpus][:num_gpus])
        
        time.sleep(60)


def vul_to_lang(cwe):
    if "py" in cwe:
        return "py"
    if "cpp" in cwe:
        return "cpp"
    if "js" in cwe:
        return "js"
    if "rb" in cwe:
        return "rb"
    if "go" in cwe:
        return "go"
    return None


def vul_to_fc_infill(cwe):
    return f"result_multiple-{vul_to_lang(cwe)}_fim.json"


def vul_to_fc_measure(cwe):
    return f"result_multiple-{vul_to_lang(cwe)}_fim.results.json"


def vul_num(cwe):
    return cwe.split("-")[1]


def opt_vul_ratio_from_json(json_path):
    return json.load(open(json_path))["eval_summary"]["opt_vul_ratio"]


def init_vul_ratio_from_json(json_path):
    return json.load(open(json_path))["eval_summary"]["init_vul_ratio"]


def baseline_vul_ratio_from_json(json_path):
    return json.load(open(json_path))["eval_summary"]["baseline_vul_ratio"]

def fc_baseline_path(vul, model):
    return f"../../sec_data/all_results/fc_baseline/{model}/temp_0.4/{vul_to_lang(vul)}"


def fc_from_json(path, baseline_path, test=False):
    res = json.load(open(path))
    ret = None
    for k in res:
        if "multiple" in k:
            ret = res[k]
            break
    if ret is None:
        print(colored(f"No multiple in keys for {path}", "red"))
        return {"pass@1": 0, "pass@10": 0}
        raise ValueError("No multiple in keys")

    if test:
        baseline = json.load(open(f"{baseline_path}/{k}_fim_test.results.json"))
    else:
        baseline = json.load(open(f"{baseline_path}/{k}_fim.results.json"))
    base = baseline[k]

    ret = {k: ret[k] / base[k] for k in ret if k in base}

    return ret

def raw_fc_from_json(path, test=False):
    res = json.load(open(path))
    ret = None
    for k in res:
        if "multiple" in k:
            ret = res[k]
            break
    if ret is None:
        print(colored(f"No multiple in keys for {path}", "red"))
        return {"pass@1": 0, "pass@10": 0}
        raise ValueError("No multiple in keys")

    ret = {k: ret[k] for k in ret}

    return ret


all_vuls = [
    "cwe-193_cpp",
    "cwe-943_py",
    "cwe-131_cpp",
    "cwe-079_js",
    "cwe-502_js",
    "cwe-020_py",
    "cwe-090_py",
    "cwe-416_cpp_p",
    "cwe-476_cpp",
    "cwe-077_rb",
    "cwe-078_py",
    "cwe-089_py",
    "cwe-022_py",
    "cwe-326_go",
    "cwe-327_py",
    "cwe-787_cpp",
]
all_attack_pos = [
    "global_prefix",
    "local_prefix",
    "line_prefix",
    "line_middle",
    "line_suffix",
    "local_suffix",
    "global_suffix",
]
