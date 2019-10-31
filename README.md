## 1. Setup

Create a template file with the command you want to run in the `template` folder. The template file contains a set of commands with arguments than will be automatically filled with the config file parameters. To define the set of parameters of your experiment, create a yaml config file containing the parameters in the `config` folder. You can define a set of parameters that are global to all the experiments in `config/default.yml`, for example the jobs logging directory, or the conda envrionment you are using. If one parameter is redefined is the user config file, then it overrides the default value.

## 2. Run
Submit a set of jobs to the scheduler with
```
python -m pyjob.launch template config.yml
```

## 3. Options
`--show-args`: show user arguments of a template.<br/>
`--no-sub`: print the list of jobs parameters without sending the jobs.<br/>

## 4. Example
Template example:
```
python -c "print('Hello {first_name} {last_name}')"
```
Config example:
```
first_name:
- Bob
- May
last_name:
- Dylan
- Jenkins
```

You should get an output similar to this one:
```
Fixed configuration on all the experiments:
{'code_dir': '/sequoia/data1/rstrudel/code', 'job_log_dir': '/sequoia/data1/rstrudel/exps', 'conda_env_name': 'robot', 'machine': 'inria', 'job_name': 'print_hello'} 

Experiments:
0: {'first_name': 'Bob', 'last_name': 'Dylan'}
Your job 7268149 ("print_hello") has been submitted
1: {'first_name': 'Bob', 'last_name': 'Jenkins'}
Your job 7268150 ("print_hello") has been submitted
2: {'first_name': 'May', 'last_name': 'Dylan'}
Your job 7268151 ("print_hello") has been submitted
3: {'first_name': 'May', 'last_name': 'Jenkins'}
Your job 7268152 ("print_hello") has been submitted

4 jobs launched.
You can check the scripts in /sequoia/data1/rstrudel/exps/scripts/print_hello_*.pbs
You can check the logs in /sequoia/data1/rstrudel/exps/print_hello.o*
```
