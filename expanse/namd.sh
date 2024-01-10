#!/bin/bash
#SBATCH --job-name="namd"
#SBATCH --output="namd.%j.%N.out"
#SBATCH --partition=compute
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --account=dxu100
#SBATCH --export=ALL
#SBATCH -t 00:10:00

#This job runs with 2 nodes, 128 cores per node for a total of 256 tasks.
NNODES=2
NCPUPERNODE=128
NCPU=$((NNODES*NCPUPERNODE))
export OMP_NUM_THREADS=${NCPU}

cd $SLURM_SUBMIT_DIR

module purge
module load cpu/0.17.3b  gcc/10.2.0/npcyll4  openmpi/4.1.3/oq3qvsv
module load namd/2.14/dstif4f

CHARMRUN=`which charmrun`
NAMD2=`which namd2`

BASENAME=basename
$CHARMRUN +p${NCPU} $NAMD2 ${BASENAME}.namd > ${BASENAME}.log
