import click
import os
import subprocess
from string import Formatter
import copy
from sklearn.model_selection import ParameterGrid
import yaml
import getpass

from pyqsub.settings import TEMPLATE_DIR, CFG_DIR, EXP_DIR


def make_dirs():
    logs_dir = os.path.join(EXP_DIR, 'logs')
    pbs_dir = os.path.join(EXP_DIR, 'scripts')
    for exp_dir in [logs_dir, pbs_dir]:
        if not os.path.exists(exp_dir):
            os.makedirs(exp_dir, exist_ok=True)


def create_template(template_dir, template_file):
    template = ''
    with open(os.path.join(template_dir, 'header.pbs'), 'r') as f:
        template = '# HEADER\n' + f.read()
    with open(os.path.join(template_dir, template_file), 'r') as f:
        template += '\n\n# EXPERIMENT\n' + f.read()
    return template


def create_list_dict_args(args, config):
    logs_dir = os.path.join(EXP_DIR, 'logs')
    if 'job_logs' not in config:
        config['job_logs'] = [logs_dir]
    if 'job_name' not in config:
        raise ValueError('job_name is not defined is config.')
    elif len(config['job_name']) > 1:
        raise ValueError('Only one job_name is allowed per experiment.')

    list_dict_args = list(ParameterGrid(config))
    for arg in args:
        if arg not in list_dict_args[0]:
            raise ValueError('{} is a template argument but is not defined.'.format(arg))
    return list_dict_args


def launch_jobs(template, list_dict_args, config, qsub):
    jobs_name = list_dict_args[0]['job_name']

    single_keys = [key for key, value in config.items() if len(value) == 1]
    multi_keys = [key for key, value in config.items() if len(value) > 1]
    print('Fixed configuration on all the experiments:')
    print({k: config[k][0] for k in single_keys}, '\n')

    print('Experiments:')
    pbs_dir = os.path.join(EXP_DIR, 'scripts')
    for i, dict_args in enumerate(list_dict_args):
        pbs_file = os.path.join(pbs_dir, '{}_{}.pbs'.format(jobs_name, i))
        with open(pbs_file, 'w') as f:
            pbs_content = template.format(**dict_args)
            f.write(pbs_content)
        print({k: dict_args[k] for k in multi_keys})
        print('Script {} written.'.format(pbs_file))
        if qsub:
            subprocess.run(['qsub', pbs_file])
    print()

    logs_dir = list_dict_args[0]['job_logs']
    user = getpass.getuser()
    if qsub:
        print('{} jobs launched.'.format(len(list_dict_args)))
    print('You can check the scripts in {}/{}_*.pbs'.format(pbs_dir, jobs_name))
    if qsub:
        print('You can check the logs in {}/{}.o*'.format(logs_dir, jobs_name))
        print('You can kill the jobs associated to that task by calling from the sequoia master node:')
        print('qstat -u {} | grep {} | grep {} | cut -d \' \' -f1 | xargs qdel'.format(user, user, jobs_name))
    else:
        print('No jobs launched!')


def parse_template(template):
    args = list(set([name for _, name, _, _ in Formatter().parse(template) if name is not None]))
    return args


def show_experiment(template, args, config_file):
    print('Template (.pbs):\n{}\n'.format(template))
    print('Arguments:\n{}\n'.format(args))
    with open(config_file) as f:
        print('Config:\n{}'.format(f.read()))


@click.command()
@click.argument('pbs-file', type=str)
@click.argument('yaml-file', type=str)
@click.option('--show/--no-show', default=False)
@click.option('--no-qsub/--no-no-qsub', default=False)
def main(pbs_file, yaml_file, show, no_qsub):
    make_dirs()
    template = create_template(TEMPLATE_DIR, pbs_file)
    args = parse_template(template)
    config_file = os.path.join(CFG_DIR, yaml_file)
    if show:
        show_experiment(template, args, config_file)
        print('Experiment not launched!')
        return

    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    list_dict_args = create_list_dict_args(args, config)
    launch_jobs(template, list_dict_args, config, not no_qsub)


if __name__ == '__main__':
    main()
