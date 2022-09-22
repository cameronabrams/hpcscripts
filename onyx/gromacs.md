Compilation of gromacs on onyx

    module swap PrgEnv-cray PrgEnv-gnu
    module swap gcc/11.2.0 gcc/9.3.0
    module load cuda
    module list

    tar zvxf gromacs-2022.1.tgz
    cd gromacs-2022.1
    mkdir build
    cd build
    cmake ..  -DGMX_BUILD_OWN_FFTW=ON -DREGRESSIONTEST_DOWNLOAD=ON -DGMX_GPU=CUDA -DCMAKE_INSTALL_PREFIX=/p/home/cfabrams/opt/gromacs/2022.1 -DGMX_MPI=ON
