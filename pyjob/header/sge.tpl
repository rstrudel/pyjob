#$ -l mem_req=8G
#$ -l h_vmem=10000G
#$ -pe serial {n_gpus}
#$ -q {queues}
#$ -e {job_log_dir}
#$ -o {job_log_dir}
#$ -N {job_name}

# avoid multithreading issues
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1