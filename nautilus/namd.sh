#SBATCH --account=ARLAP35100034
#SBATCH --partition=general
#SBATCH --qos=standard
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=128
#SBATCH --time=02:00:00
#SBATCH --job-name=scale1
#SBATCH --export=ALL

module unload amd/aocc/4.0.0  amd/aocl/aocc/4.0  penguin/openmpi/4.1.4/aocc
module load intel/compiler/latest
module load penguin/openmpi/4.1.5/intel

cd $SLURM_SUBMIT_DIR

CHARMRUN=/p/home/cfabrams/build/NAMD_2.14_Source/Linux-x86_64-icc/charmrun
NAMD2=/p/home/cfabrams/build/NAMD_2.14_Source/Linux-x86_64-icc/namd2

CONFIG=my.namd
LOG=my.log

$CHARMRUN +p${NCPU} $NAMD2 $CONFIG > $LOG
