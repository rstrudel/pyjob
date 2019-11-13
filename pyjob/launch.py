import click
import os
import subprocess
import getpass
from termcolor import colored

from pyjob.utils import get_scheduler_infos, make_dirs, create_template, parse_template, load_config
from pyjob.utils import create_args_from_config, show_submission


def launch_jobs(scheduler_infos, template, list_dict_args, config, submit):
    jobs_name = list_dict_args[0]['job_name']
    job_log_dir = list_dict_args[0]['job_log_dir']
    job_extension = scheduler_infos['extension']

    single_keys = [key for key, value in config.items() if len(value) == 1]
    multi_keys = [key for key, value in config.items() if len(value) > 1]
    print('Fixed configuration on all the experiments:')
    print({k: config[k][0] for k in single_keys}, '\n')

    print('Experiments:')
    template_dir = os.path.join(job_log_dir, 'scripts')
    for i, dict_args in enumerate(list_dict_args):
        template_file = os.path.join(template_dir, '{}_{}.{}'.format(jobs_name, i, job_extension))
        with open(template_file, 'w') as f:
            template_content = template.format(**dict_args)
            f.write(template_content)
        print('{}: {}'.format(i, {k: dict_args[k] for k in multi_keys}))
        if submit:
            subprocess.run([scheduler_infos['submit_command'], template_file])
    print()

    user = getpass.getuser()
    if submit:
        print('{} jobs launched.'.format(len(list_dict_args)))
    print('You can check the scripts in {}/{}_*.{}'.format(template_dir, jobs_name, job_extension))
    if submit:
        print('You can check the logs in {}/{}.o*'.format(job_log_dir, jobs_name))
        print('You can kill the jobs associated to that task by calling:')
        # print('qstat -u {} | grep {} | grep {} | cut -d \' \' -f1 | xargs qdel'.format(user, user, jobs_name))
    else:
        print('No jobs launched!')


@click.command()
@click.argument('template-file', type=str)
@click.argument('config-file', type=str)
@click.option('--scheduler', '-sched', default='sge', type=str)
@click.option('--show/--no-show', default=False)
@click.option('--sub/--no-sub', default=True)
def main(template_file, config_file, scheduler, show, sub):
    scheduler_infos = get_scheduler_infos(scheduler)
    template = create_template(scheduler_infos, template_file)
    template_args = parse_template(template)
    config = load_config(scheduler_infos, config_file)
    make_dirs(config['job_log_dir'][0])
    if show:
        show_submission(template, template_args, config)
        print('Experiment not launched!')
    else:
        list_dict_args = create_args_from_config(template_args, config)
        launch_jobs(scheduler_infos, template, list_dict_args, config, sub)


if __name__ == '__main__':
    main()
