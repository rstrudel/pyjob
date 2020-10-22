#$ -l mem_req=8G
#$ -l h_vmem=10000G
#$ -pe serial {n_gpus}
#$ -q {queues}
#$ -e {job_log_dir}
#$ -o {job_log_dir}
#$ -N {job_name}

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