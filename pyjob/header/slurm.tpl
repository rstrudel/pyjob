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

# conda
. {conda_dir}/etc/profile.d/conda.sh
export LD_LIBRARY_PATH={conda_dir}/envs/bin/lib:$LD_LIBRARY_PATH
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# avoid multithreading issues
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1

# avoid NCCL issues
export NCCL_P2P_DISABLE=1
