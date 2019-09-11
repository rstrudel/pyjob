## 1. Setup

Create a `log`, `template` and a `config` directory, set their path in `pyqsub.settings`. 
`log` contains the workers stdout and stderr.
`pbs` contains the pbs template files with the commands to run and user arguments to be defined.
`config` contains the yaml config files with the combination of user defined arguments.

## 2. Run
Send a series of job to the scheduler with
```
python -m pyqsub.launch name_template.pbs name_config.yml
```

## 3. Options
`--show-args`: show user arguments of a template.
`--no-qsub`: print the list of jobs parameters without sending the jobs.
