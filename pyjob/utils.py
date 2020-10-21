import os
from pathlib import Path
import subprocess
from string import Formatter
import yaml
from termcolor import colored

from sklearn.model_selection import ParameterGrid

BASE_DIR = Path(__file__).parent

SCHEDULER_PARAMS = {
    "sge": {
        "header": "header.pbs",
        "extension": "pbs",
        "submit_command": "qsub",
        "submit_option": "",
        "config": "default_sge.yml",
    },
    "slurm": {
        "header": "header.slurm",
        "extension": "slurm",
        "submit_command": "sbatch",
        "submit_option": "",
        "config": "default_slurm.yml",
    },
    "oar": {
        "header": "header.oar",
        "extension": "oar",
        "submit_command": "oarsub",
        "submit_option": "--scanscript",
        "config": "default_oar.yml",
    },
}

COLORS = {"t1": "yellow", "t2": "red"}


def launch_jobs(scheduler_infos, template, list_dict_args, config, submit):
    jobs_name = list_dict_args[0]["job_name"]
    job_log_dir = Path(list_dict_args[0]["job_log_dir"]).expanduser()
    job_extension = scheduler_infos["extension"]

    # seperate fixed keys from changing ones
    single_keys = [key for key, value in config.items() if len(value) == 1]
    multi_keys = [key for key, value in config.items() if len(value) > 1]
    print_color("Fixed parameters:", COLORS["t1"])
    print_dict({k: config[k][0] for k in single_keys})

    print_color("Experiments:", COLORS["t1"])
    template_dir = job_log_dir / "scripts"
    template_dir.mkdir(exist_ok=True, parents=True)
    for i, dict_args in enumerate(list_dict_args):
        template_file = template_dir / f"{jobs_name}_{i}.{job_extension}"
        template_content = template.format(**dict_args)
        with open(template_file, "w") as f:
            f.write(template_content)
        print_color(i, COLORS["t2"])
        print_dict({k: dict_args[k] for k in multi_keys})
        processes = []
        if submit:
            args_run = [scheduler_infos["submit_command"], template_file]
            submit_option = scheduler_infos["submit_option"]
            if submit_option:
                args_run.insert(1, submit_option)
            subprocess.run(args_run)
            # p = subprocess.Popen(args_run)
            # processes.append(p)
    # for i, p in enumerate(processes):
    #     print(i)
    #     p.wait()
    print()

    if submit:
        print(f"{len(list_dict_args)} jobs launched.")
    print(f"You can check the scripts in {template_dir}/{jobs_name}_*.{job_extension}")

    if submit:
        print(
            f"You can check the logs in {job_log_dir}. A job output is stored as {jobs_name}.o* and its errors as {jobs_name}.e* ."
        )
    else:
        print("No jobs launched!")


def create_template(scheduler_infos, template):
    header_file = BASE_DIR / "header" / scheduler_infos["header"]
    template_file = BASE_DIR / "template" / template

    template = ""
    with open(header_file, "r") as f:
        template = f.read()
    with open(template_file, "r") as f:
        template += "\n\n# EXPERIMENT\n" + f.read()
    return template


def parse_template(template):
    args = list(
        set([name for _, name, _, _ in Formatter().parse(template) if name is not None])
    )
    return args


def expand_config(config):
    # expand lists in a range
    for k, v in config.items():
        if len(v) == 1 and isinstance(v[0], list):
            expanded_v = list(range(v[0][0], v[0][1]))
            config[k] = expanded_v
    return config


def load_config(schduler_infos, config_file):
    default_config_file = BASE_DIR / "config" / schduler_infos["config"]
    user_config_file = BASE_DIR / "config" / config_file
    with open(default_config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    with open(user_config_file) as f:
        user_config = yaml.load(f, Loader=yaml.FullLoader)
    config.update(user_config)
    config = expand_config(config)

    required_args = ["job_log_dir", "job_name"]
    for arg in required_args:
        if arg not in config:
            raise ValueError("{} should be defined in config.".format(arg))

    # allow job log dir in home directory
    config["job_log_dir"][0] = str(Path(config["job_log_dir"][0]).expanduser())

    if len(config["job_name"]) > 1:
        raise ValueError("Only one job_name is allowed per experiment.")

    return config


def args_from_config(template_args, config):
    unused_config_args = {
        arg: v for arg, v in config.items() if arg not in template_args
    }
    config = {k: v for k, v in config.items() if k not in unused_config_args}

    list_dict_args = list(ParameterGrid(config))
    for arg in template_args:
        if arg not in list_dict_args[0]:
            raise ValueError(
                f"{arg} is a template argument but is not defined in config."
            )
    return list_dict_args, unused_config_args


def show_submission(template, args, config):
    color = COLORS["t1"]
    print_color("Template:", color)
    print(f"{template}\n")
    print_color("Arguments:", color)
    print(f"{args}\n")
    print_color("Config:", color)
    print_dict(config)


def print_dict(d):
    for k, v in d.items():
        print(f"{k}: {v}")


def print_color(s, color):
    print(colored(s, color))
