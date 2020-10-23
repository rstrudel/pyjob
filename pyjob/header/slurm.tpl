#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --ntasks=1
#SBATCH --partition={queue}
#SBATCH --qos={qos}
#SBATCH --gres=gpu:{n_gpus}
#SBATCH --cpus-per-task={n_cpus}

#SBATCH --hint=nomultithread
#SBATCH --time={time}
#SBATCH --output={job_log_dir}/{job_name}.o%j
#SBATCH --error={job_log_dir}/{job_name}.e%j

# cleaning modules launched during interactive mode
module purge

