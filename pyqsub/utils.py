import os
from sklearn.model_selection import ParameterGrid
import yaml
from string import Formatter

from pyqsub.settings import BASE_DIR


def get_scheduler_infos(scheduler):
    scheduler_dict = {
        'sge': {
            'header': 'header.pbs',
            'extension': 'pbs',
            'submit_command': 'qsub'
        },
        'slurm': {
            'header': 'header.slurm',
            'extension': 'slurm',
            'submit_command': 'sbatch'
        }
    }
    if scheduler not in scheduler_dict:
        raise ValueError('{} is an unknown scheduler. Supported schedulers: {}'.format(
            scheduler, scheduler_dict.keys()))
    return scheduler_dict[scheduler]


def make_dirs(jobs_log_dir):
    scripts_dir = os.path.join(jobs_log_dir, 'scripts')
    for exp_dir in scripts_dir:
        if not os.path.exists(exp_dir):
            os.makedirs(exp_dir, exist_ok=True)


def create_template(scheduler_infos, template):
    header_file = os.path.join(BASE_DIR, 'header', scheduler_infos['header'])
    template_file = os.path.join(BASE_DIR, 'template', template)

    template = ''
    with open(header_file, 'r') as f:
        template = f.read()
    with open(template_file, 'r') as f:
        template += '\n\n# EXPERIMENT\n' + f.read()
    return template


def parse_template(template):
    args = list(set([name for _, name, _, _ in Formatter().parse(template) if name is not None]))
    return args


def load_config(config_file):
    default_config_file = os.path.join(BASE_DIR, 'config', 'default.yml')
    user_config_file = os.path.join(BASE_DIR, 'config', config_file)
    with open(default_config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    with open(user_config_file) as f:
        user_config = yaml.load(f, Loader=yaml.FullLoader)
    config.update(user_config)

    required_args = ['job_log_dir', 'job_name']
    for arg in required_args:
        if arg not in config:
            raise ValueError('{} should be defined in config.'.format(arg))
    if len(config['job_name']) > 1:
        raise ValueError('Only one job_name is allowed per experiment.')
    return config


def create_args_from_config(template_args, config):
    list_dict_args = list(ParameterGrid(config))
    for arg in template_args:
        if arg not in list_dict_args[0]:
            raise ValueError('{} is a template argument but is not defined in config.'.format(arg))
    return list_dict_args


def show_submission(template, args, config_file):
    color = 'yellow'
    print(colored('Template:', color))
    print('{}\n'.format(template))
    print(colored('Arguments:', color))
    print('{}\n'.format(args))
    print(colored('Config:', color))
    with open(config_file) as f:
        print('{}'.format(f.read()))
