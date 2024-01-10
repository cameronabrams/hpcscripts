#!/bin/bash
#SBATCH -N 1
#SBATCH --ntasks-per-node=40
#SBATCH -p GPU
#SBATCH -t 24:00:00
#SBATCH --gres=gpu:v100:8
#
set echo
set -x
# Load the needed modules
module load namd/2.13-gpu
BASENAME=prod_ds1
cd $SLURM_SUBMIT_DIR
echo $SLURM_NTASKS
$BINDIR/namd2 +setcpuaffinity +p 40 +devices 0,1,2,3,4,5,6,7 ${BASENAME}.namd > ${BASENAME}.log

