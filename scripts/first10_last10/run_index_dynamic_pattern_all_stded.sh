#!/bin/bash
#SBATCH --job-name=all_stded index
#SBATCH --partition=compute
#SBATCH --nodes=12
#SBATCH --ntasks-per-node=128
#SBATCH --exclusive
#SBATCH --time=00:60:00
#SBATCH --mail-type=FAIL
#SBATCH --account=mh0033
#SBATCH --output=all_stded_index.%j.out

# limit stacksize ... adjust to your programs need
# and core file size
ulimit -s 204800
ulimit -c 0

set -e 
ls -l
srun python ./index_dynamic_pattern_all_stded.py