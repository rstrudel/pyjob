# pyjob

Simple library to launch batched jobs and run grid-search over parameters seamlessly. It includes multiple schedulers such as `sge`, `slurm` and `oar`. Given lists of parameters, it computes a cartesian product based on [sklearn.model_selection.ParameterGrid](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.ParameterGrid.html) and launch one job for each combination in the parameters grid.<br/>

## 1. Install

To install, run:
```
pip install git+https://github.com/rstrudel/pyjob.git@master#egg=pyjob
```


## 2. Run
To test `pyjob`, you can directly run "Hello world" jobs with :
```
python -m pyjob.launch example/hello.tpl example/hello.yml --scheduler slurm
```

To try `pyjob` on your own experiments check Section 3, to check how the "Hello World" example was built check Section 4, to use conda environments check Section 5 and to use `pyjob` for distributed training, check Section 7. Once set up, with only one command you will be able to submit a set of jobs defined by a template:

```
python train.py --learning-rate {lr} --weight-decay {weight_decay} --dropout {dropout}
```

Over a grid of learning rate, weight decay and dropout parameters defined in a configuration file.

## 3. Create an experiment

In the `template` folder, create a template file `experiment_name` with the command you want to run. Parameters defined with the configuration file should be put inside curly brackets \{\}.<br/>
In the `config` folder, create a yaml configuration file `experiment_name.yml` containing the field of values of the variables between curly brackets.<br/>

Run:

```
python -m pyjob.launch experiment_name experiment_name.yml --scheduler slurm
```

You can define a set of parameters that are global to all the experiments in `config/default_slurm.yml`, for example the jobs logging directory `job_log_dir`, the job queue `queue` or the conda envrionment you are using and so on. If one parameter is redefined in the user configuration file, then it overrides the default configuration.


## 4. Example: Hello World
Template `hello.tpl`:
```
python -c "print('Hello {first_name} {last_name}')"
```
The script requires `first_name` and `last_name` to be defined.


Configuration `hello.yml`:
```
job_name:
- hello
first_name:
- Bob
- Maria
last_name:
- Dylan
- Casares
```
The configuration file defines the set of values taken by `first_name` and `last_name`.

By running `python -m pyjob.launch hello hello.yml --scheduler slurm`, you should get an output similar to this one:
```
Fixed parameters:
queue: gpu_p1
qos: qos_gpu-t3
n_gpus: 1
n_cpus: 10
time: 20:00:00
job_log_dir: pyjob/
job_name: hello
Experiments:
0
first_name: Bob
last_name: Dylan
Submitted batch job 555789
1
first_name: Bob
last_name: Casares
Submitted batch job 555790
2
first_name: Maria
last_name: Dylan
Submitted batch job 555791
3
first_name: Maria
last_name: Casares
Submitted batch job 555792

4 jobs launched.
You can check the scripts in ~/pyjob/scripts/hello_*.slurm
You can check the logs in ~/pyjob/. A job output is stored as hello.o* and its errors as hello.e*.
```

## 5. Anaconda

If you want to load conda, you first need to add `conda_dir` to your configuration file.
`conda_dir` can be defined globally, just create a file `slurm.yml` containing `conda_dir` and it will be used for every experiments using `slurm` scheduler.

Once set you can add `conda activate {env_name}` to your template and update your configuration accordingly.


`conda_dir` should be defined in `config/default_slurm.yml`, then at the top of your template you can add `conda activate {conda_env_name}` and either define the environment name in your configuration or directly in the template file.

## 6. Options
`--no-sub`: print the list of jobs parameters without submitting the jobs.<br/>
`--show`: print a template and configuration file without submitting the jobs.<br/>


## 7. Distributed training

You may want to run distributed training over multiples nodes on a cluster. If you are using [PyTorch](https://pytorch.org/) distributed library, the distributed processes can be initialized using a file with:
```
dist.init_process_group(
    backend,
    init_method=f"file://{sync_file}",
    rank=node_rank,
    world_size=world_size,
)
```
`sync_file` is the same synchronization file for every node while `node_rank` defines the global rank of a node and `world_size` the total number of nodes. You can change your argparse/click script to add `dist_rank` and `world_size` as arguments and adapt the template and configuration file easily:

Template `template/distributed`:
```
python train.py --learning-rate {lr} --node-rank {node_rank} --world-size {world_size}
```

Configuration `config/distributed.yml`:
```
lr:
- 0.001
- 0.005
node_rank:
- [0, 4]
world_size:
- 4
```

This will run each experiment using 4 nodes resulting in 8 batched jobs.
