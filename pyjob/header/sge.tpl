#$ -l mem_req={mem_req}
#$ -l h_vmem={h_vmem}
#$ -pe serial {n_gpus}
#$ -q {queues}
#$ -e {job_log_dir}
#$ -o {job_log_dir}
#$ -N {job_name}

# avoid multithreading issues
export MKL_NUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export OMP_NUM_THREADS=1