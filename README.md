
## 1. Run
Submit a set of jobs to the scheduler with
```
python -m pyjob.launch template config.yml
```

## 2. Options
`--show`: show arguments of a template without submitting the jobs.<br/>
`--no-sub`: print the list of jobs parameters without submitting the jobs.<br/>

## 3. Create an experiment

Create a template file with the command you want to run in the `template` folder.<br/>
Create a yaml config file with the parameters you want to set in the `config` folder.<br/>

You can define a set of parameters that are global to all the experiments in `config/default.yml`, for example the jobs logging directory, or the conda envrionment you are using. If one parameter is redefined is the user config file, then it overrides the default value.

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

By running `python -m pyjob.launch hello hello.yml`, you should get an output similar to this one:
```
Fixed configuration on all the experiments:
{'code_dir': '/sequoia/data1/rstrudel/code', 'job_log_dir': '/sequoia/data1/rstrudel/exps', 'job_name': 'print_hello'} 

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
