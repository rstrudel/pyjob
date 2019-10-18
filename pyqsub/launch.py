import click
import os
import subprocess
from string import Formatter
import copy
from sklearn.model_selection import ParameterGrid
import yaml

from pyqsub.settings import LOG_DIR, PBS_DIR, CFG_DIR


def create_template(pbs_dir, pbs_file):
    template = ''
    with open(os.path.join(pbs_dir, 'header.pbs'), 'r') as f:
        template = '# HEADER\n' + f.read()
    with open(os.path.join(pbs_dir, pbs_file), 'r') as f:
        template += '\n\n# EXPERIMENT\n' + f.read()
    return template


def launch_jobs(template, args, config, no_qsub):
    # write pbs and launch jobs
    list_dict_args = list(ParameterGrid(config))
    for arg in args:
        assert arg in list_dict_args[
            0], '{} is needed by the template but is not defined.'.format(arg)

    pbs_file = 'temp.pbs'
    for dict_args in list_dict_args:
        print(dict_args)
        with open(pbs_file, 'w') as f:
            pbs_content = template.format(**dict_args)
            f.write(pbs_content)
        if not no_qsub:
            subprocess.run(['qsub', pbs_file])
    # os.remove(pbs_file)
    if not no_qsub:
        print('{} jobs launched.'.format(len(list_dict_args)))


def parse_template(template):
    args = list(
        set([
            name for _, name, _, _ in Formatter().parse(template)
            if name is not None
        ]))
    return args


def show_experiment(template, args, config_file):
    print('Arguments:\n{}\n'.format(args))
    with open(config_file) as f:
        print('Config:\n{}\n'.format(f.read()))
    print('Template (.pbs):\n{}'.format(template))


@click.command()
@click.argument('pbs-file', type=str)
@click.argument('yaml-file', type=str)
@click.option('--show/--no-show', default=False)
@click.option('--no-qsub/--no-no-qsub', default=False)
def main(pbs_file, yaml_file, show, no_qsub):
    # create pbs string
    template = create_template(PBS_DIR, pbs_file)
    args = parse_template(template)
    config_file = os.path.join(CFG_DIR, yaml_file)
    if show:
        show_experiment(template, args, config_file)
        print('Experiment not launched!')
        return

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    launch_jobs(template, args, config, no_qsub)


if __name__ == '__main__':
    main()
