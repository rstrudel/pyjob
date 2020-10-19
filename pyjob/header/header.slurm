#!/bin/bash
#SBATCH --job-name={job_name}
#SBATCH --ntasks=1
#SBATCH --partition={queue}
#SBATCH --qos={qos}
#SBATCH --gres=gpu:{n_gpus}
#SBATCH --cpus-per-task={n_cpus}

#SBATCH --hint=nomultithread
#SBATCH --time={time}
#SBATCH --output={job_log_dir}/%j.out
#SBATCH --error={job_log_dir}/%j.err

# cleaning modules launched during interactive mode
module purge

# loading modules
module load anaconda-py3/2019.03

# avoid multithreading issues
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

# avoid NCCL issues
export NCCL_P2P_DISABLE=1
