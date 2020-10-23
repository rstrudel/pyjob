#! /bin/bash

#OAR -n {job_name}
#OAR -t {job_type_0}
#OAR -t {job_type_1}
#OAR -l walltime={walltime}
#OAR --stdout {job_log_dir}/{job_name}.out
#OAR --stderr {job_log_dir}/{job_name}.err

# Set GPU visible
source gpu_setVisibleDevices.sh
