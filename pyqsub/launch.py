import click
import os
import subprocess
from string import Formatter
import copy
from sklearn.model_selection import ParameterGrid
import yaml

from pyqsub.settings import LOG_DIR, PBS_DIR, CFG_DIR


def create_pbs_template(pbs_dir, pbs_file):
    pbs_template = ''
    with open(os.path.join(pbs_dir, 'header.pbs'), 'r') as f:
        pbs_template = f.read()
    with open(os.path.join(pbs_dir, pbs_file), 'r') as f:
        pbs_template += f.read()
    return pbs_template


def launch_jobs(pbs_template, pbs_args, user_dict_args, no_qsub):
    # write pbs and launch jobs
    list_dict_args = list(ParameterGrid(user_dict_args))
    for arg in pbs_args:
        assert arg in list_dict_args[
            0], '{} is needed by pbs but is not defined.'.format(arg)

    pbs_file = 'temp.pbs'
    for dict_args in list_dict_args:
        print(dict_args)
        with open(pbs_file, 'w') as f:
            pbs_content = pbs_template.format(**dict_args)
            f.write(pbs_content)
        if not no_qsub:
            subprocess.run(['qsub', pbs_file])
    os.remove(pbs_file)


@click.command()
@click.argument('pbs-file', type=str)
@click.argument('yaml-file', type=str)
@click.option('--show-args/--no-show-args', default=False)
@click.option('--no-qsub/--no-no-qsub', default=False)
def main(pbs_file, yaml_file, show_args, no_qsub):
    # create pbs string
    pbs_template = create_pbs_template(PBS_DIR, pbs_file)
    pbs_args = list(
        set([
            name for _, name, _, _ in Formatter().parse(pbs_template)
            if name is not None
        ]))
    if show_args:
        print('Pbs Arguments: {}'.format(pbs_args))
        print('Pbs Template:\n {}'.format(pbs_template))
        return

    with open(os.path.join(CFG_DIR, yaml_file)) as f:
        user_dict_args = yaml.load(f, Loader=yaml.FullLoader)
    launch_jobs(pbs_template, pbs_args, user_dict_args, no_qsub)


if __name__ == '__main__':
    main()
