## 1. Setup

Create a template file with the command you want to run in the `template` folder. The template file conrains a set of commands with arguments than will be automatically filled with the config file parameters. To define the set of parameters of your experiment, create a yaml config file containing the parameters in the `config` folder. You can define a set of parameters that are global to all the experiments in `config/default.yml`, for example the jobs logging directory, or the conda envrionment you are using. If one parameter is redefined is the user config file, then it overrides the default value.

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
python -c "print('Hello {} {}'.format({first_name}, {last_name}))"
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

It should run 4 jobs as it will run all the possible combinations of parameters. The output of each job will be:
```
Hello Bob Dylan
Hello Bob Jenkins
Hello May Dylan
Hello May Jenkins
```
