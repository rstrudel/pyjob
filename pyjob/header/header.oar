#! /bin/bash

#OAR -n {job_name}
#OAR -t {job_type_0}
#OAR -t {job_type_1}
#OAR -l walltime={walltime}
#OAR --stdout {job_log_dir}/{job_name}.out
#OAR --stderr {job_log_dir}/{job_name}.err
#OAR -p host!='gpuhost10'

# Set GPU visible
source gpu_setVisibleDevices.sh

# conda
export LC_ALL=C.UTF-8
export LANG=C.UTF-8
