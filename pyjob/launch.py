import os
from pathlib import Path

import click

from pyjob.utils import (
    launch_jobs,
    create_template,
    parse_template,
    load_config,
    args_from_config,
    print_color,
    print_dict,
    show_submission,
    SCHEDULER_PARAMS,
    COLORS,
)


def setup_experiment(scheduler, template_file, config_file, directory):
    # load template and config
    scheduler_infos = SCHEDULER_PARAMS[scheduler]
    config = load_config(scheduler_infos, config_file, directory)
    load_conda = "conda_dir" in config
    template = create_template(scheduler_infos, template_file, directory, load_conda)
    template_args = parse_template(template)

    return scheduler_infos, template, template_args, config


@click.command()
@click.argument("template-file", type=str)
@click.argument("config-file", type=str)
@click.option("--scheduler", "-sched", required=True, type=str)
@click.option("--show/--no-show", default=False)
@click.option("--sub/--no-sub", default=True)
@click.option("--directory", "-dir", default="", type=str)
def main(template_file, config_file, scheduler, show, sub, directory):
    if scheduler not in SCHEDULER_PARAMS.keys():
        raise ValueError(
            f"{scheduler} is an unknown scheduler. Supported schedulers: {SCHEDULER_PARAMS.keys()}"
        )

    scheduler_infos, template, template_args, config = setup_experiment(
        scheduler, template_file, config_file, directory
    )

    # show experiments and run
    if show:
        show_submission(template, template_args, config)
        print("\nExperiment not launched!")
        return

    list_dict_args, unused_args = args_from_config(template_args, config)
    if unused_args:
        print_color("Unused parameters:", COLORS["t1"])
        print_dict(unused_args)
    launch_jobs(scheduler_infos, template, list_dict_args, config, sub)


if __name__ == "__main__":
    main()
