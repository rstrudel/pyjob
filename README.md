## 1. Setup

Create a `log`, `template` and a `config` directory, set their path in `pyqsub.settings`.<br/>
`log` contains the workers stdout and stderr.<br/>
`template` contains the pbs template files with the commands to run and user arguments to be defined.<br/>
`config` contains the yaml config files with the combination of user defined arguments.<br/>

## 2. Run
Send a series of job to the scheduler with
```
python -m pyqsub.launch name_template.pbs name_config.yml
```

## 3. Options
`--show-args`: show user arguments of a template.<br/>
`--no-qsub`: print the list of jobs parameters without sending the jobs.<br/>
