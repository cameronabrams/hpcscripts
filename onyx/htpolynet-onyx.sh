#!/bin/bash -l
# This is a template qsub script for onyx.erdc.hpc.mil
# Cameron F. Abrams cfa22@drexel.edu

#PBS -A ARLAP35100034
#PBS -q standard
#PBS -l select=1:ncpus=44:mpiprocs=44
#PBS -l walltime=24:00:00
#PBS -N HTPOLY
#PBS -j oe
#PBS -V
#PBS -S /bin/bash
#PBS -m be
#PBS -M cfa22@drexel.edu

DIAG="diagnostics.log"
CONFIG="SYSTEM.yaml"
LOG="console.log"

cd $PBS_O_WORKDIR
conda activate mol-env
source /p/home/cfa/opt/gromacs/2022.1/bin/GMXRC.bash
htpolynet run -diag ${DIAG} ${CONFIG} &> ${LOG}
