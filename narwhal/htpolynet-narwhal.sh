#!/bin/bash -l
# This is a template qsub script for narwhal.navydsrc.hpc.mil
# Cameron F. Abrams cfa22@drexel.edu

#PBS -A ARLAP35100034
#PBS -q standard
#PBS -l select=1:ncpus=128:mpiprocs=128
#PBS -l walltime=24:00:00
#PBS -N HTPOLY
#PBS -j oe
#PBS -V
#PBS -S /bin/bash
#PBS -m be
#PBS -M cfa22@drexel.edu

DIAG="diagnostics.log"
CONFIG="DGE-PAC.yaml"
LOG="info.log"

cd $PBS_O_WORKDIR
conda activate mol-env
source /app/gromacs/gromacs-2022/bin_cpu/GMXRC.bash
htpolynet run -diag ${DIAG} ${CONFIG} &> ${LOG}
