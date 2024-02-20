#!/bin/bash
#SBATCH --account=abramsPrj
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=48
#SBATCH -p def
#SBATCH --time=20:00:00
#SBATCH --job-name=TF01

module load shared
module load DefaultModules
module load default-environment
module load gcc/9.2.0
module load slurm/picotte/21.08.8
module load intel/mkl/2020
module load cuda11.4/toolkit/11.4.2
module load fftw3/intel/2020/3.3.10
module load ucx/1.14.0-rc6
module load intel/composerxe/2020u4
module load picotte-openmpi/intel/2020/4.1.4


NNODES=8
NCPUPERNODE=48
NCPU=$((NNODES*NCPUPERNODE))
export OMP_NUM_THREADS=${NCPU}

cd $SLURM_SUBMIT_DIR
BASENAME=prod_trifppr6-r1
NAMDDIR=/ifs/groups/abramsGrp/opt/NAMD_2.14_Linux-x86_64-mpi-icc
NAMD2=${NAMDDIR}/namd2
CHARMRUN=${NAMDDIR}/charmrun
$CHARMRUN $NAMD2 +p${NCPU} +setcpuaffinity ${BASENAME}.namd > ${BASENAME}-n${NCPU}.log

