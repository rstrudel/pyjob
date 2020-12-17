#!/bin/bash
#SBATCH --job-name={job_name}

#SBATCH -C {queue}
#SBATCH --qos={qos}

#SBATCH --nodes={nodes}
#SBATCH --ntasks-per-node={gpus_per_node}
#SBATCH --gres=gpu:{gpus_per_node}
#SBATCH --cpus-per-task={cpus_per_gpu}
#SBATCH --hint=nomultithread

#SBATCH --time={time}
#SBATCH --output={job_log_dir}/{job_name}.o%j
#SBATCH --error={job_log_dir}/{job_name}.e%j

# cleaning modules launched during interactive mode
module purge
