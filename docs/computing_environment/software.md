# Software Available on NMTHPC

NMTHPC provides a wide range of scientific and research software. This page explains how to find and use available software.

## Environment Modules System

NMTHPC uses the **Environment Modules** system to manage software. Modules allow you to easily load and switch between different software packages and versions.

### Basic Module Commands

**List available modules**:
```bash
$ module avail
```

**Search for specific software**:
```bash
$ module avail python
$ module avail cuda
```

**Load a module**:
```bash
$ module load python/3.11
```

**List currently loaded modules**:
```bash
$ module list
```

**Unload a module**:
```bash
$ module unload python/3.11
```

**Unload all modules**:
```bash
$ module purge
```

**Display module information**:
```bash
$ module show python/3.11
```

**Get help with modules**:
```bash
$ module help
```

### Module Loading Best Practices

1. **Load modules in your job scripts**: Always load required modules in your SLURM scripts
2. **Specify versions**: Use specific versions for reproducibility (e.g., `python/3.11` not just `python`)
3. **Check dependencies**: Some modules automatically load dependencies
4. **Clean environment**: Use `module purge` before loading modules to avoid conflicts

## Software Categories

### Compilers

**GCC (GNU Compiler Collection)**:
```bash
$ module load gcc/11.2.0
```

**Intel Compilers**:
```bash
$ module load intel/2023
```

**NVIDIA HPC SDK** (includes nvcc for CUDA):
```bash
$ module load nvhpc/23.1
```

### Programming Languages

**Python**:
```bash
$ module load python/3.11
```

See [Python and Jupyter Notebooks](../software/python_jupyter.md) for detailed information.

**R**:
```bash
$ module load r/4.3.0
```

See [R](../software/r.md) for detailed information.

**Julia**:
```bash
$ module load julia/1.9
```

### Parallel Computing Libraries

**OpenMPI**:
```bash
$ module load openmpi/4.1.4
```

**MPICH**:
```bash
$ module load mpich/4.0
```

**Intel MPI**:
```bash
$ module load intel-mpi/2021.6
```

See [Using MPI with Fortran](../software/mpi_fortran.md) for MPI programming examples.

### GPU Computing

**CUDA Toolkit**:
```bash
$ module load cuda/12.1
```

**cuDNN** (Deep Learning library):
```bash
$ module load cudnn/8.9
```

**TensorRT** (Inference optimization):
```bash
$ module load tensorrt/8.6
```

### Mathematical and Scientific Libraries

**BLAS/LAPACK** (Linear algebra):
```bash
$ module load openblas/0.3.21
```

**FFTW** (Fast Fourier Transform):
```bash
$ module load fftw/3.3.10
```

**HDF5** (Hierarchical data format):
```bash
$ module load hdf5/1.14.0
```

**NetCDF**:
```bash
$ module load netcdf/4.9.0
```

### Machine Learning Frameworks

**TensorFlow**:
```bash
$ module load tensorflow/2.13-gpu
```

**PyTorch**:
```bash
$ module load pytorch/2.0-gpu
```


### Scientific Applications

**MATLAB**:
```bash
$ module load matlab/R2023a
```

See [MATLAB](../software/matlab.md) for usage instructions.

**VASP** (Vienna Ab initio Simulation Package):
```bash
$ module load vasp/6.4.0
```

See [VASP](../software/vasp.md) for computational chemistry examples.

**GROMACS** (Molecular dynamics):
```bash
$ module load gromacs/2023.1
```

**LAMMPS** (Molecular dynamics):
```bash
$ module load lammps/2023
```

**QuantumESPRESSO**:
```bash
$ module load quantum-espresso/7.2
```

### Data Analysis and Visualization

**Paraview**:
```bash
$ module load paraview/5.11
```

**Visit**:
```bash
$ module load visit/3.3.3
```

**ImageMagick**:
```bash
$ module load imagemagick/7.1
```

### Bioinformatics

**BLAST**:
```bash
$ module load blast/2.14.0
```

**SAMtools**:
```bash
$ module load samtools/1.17
```

**Bowtie2**:
```bash
$ module load bowtie2/2.5.1
```

## Python Package Management

### Using pip with User Installation

Install packages in your home directory:
```bash
$ module load python/3.11
$ pip install --user packagename
```

### Using Anaconda/Miniconda

Anaconda is recommended for managing Python environments:
```bash
$ module load anaconda3
$ conda create -n myenv python=3.11
$ conda activate myenv
$ conda install numpy scipy matplotlib
```

See [Anaconda](../software/anaconda.md) for comprehensive instructions.

## R Package Installation

Install R packages in your home directory:
```bash
$ module load r/4.3.0
$ R
> install.packages("ggplot2", repos="https://cloud.r-project.org")
```

See [R](../software/r.md) for more details.

## Containers (Singularity/Apptainer)

For software not available as modules, consider using containers:

```bash
$ module load apptainer
$ singularity pull docker://ubuntu:22.04
$ singularity shell ubuntu_22.04.sif
```

**Advantages**:

- Use software from Docker Hub
- Create reproducible environments
- Run complex software stacks

## Compiling Your Own Software

You can compile software in your home directory:

```bash
$ module load gcc/11.2.0
$ ./configure --prefix=$HOME/software/myapp
$ make
$ make install
```

**Tips**:

- Install to `$HOME/software` or similar directory
- Load required modules before compiling
- Add installation directory to PATH in your `~/.bashrc`

## Requesting New Software

If you need software that's not currently installed:

1. Check if containers are an option
2. Try installing in your home directory
3. Contact HPC support at <hpc@nmthpc.atlassian.net> with:
   - Software name and version
   - Website or download link
   - Brief description of your use case
   - Whether it requires a license

We'll evaluate requests for system-wide installation.

## Module Files in Your Job Scripts

Always load required modules in your SLURM scripts:

```bash
#!/bin/bash
#SBATCH --job-name=my_job
#SBATCH --ntasks=4
#SBATCH --time=01:00:00

# Load required modules
module purge
module load gcc/11.2.0
module load openmpi/4.1.4
module load python/3.11

# Run your application
python my_script.py
```

## Software Versions

```{note}
Software versions listed on this page are examples. Use `module avail` to see currently installed versions on NMTHPC.
```

## License-Restricted Software

Some software requires licenses:

- **MATLAB**: Check license availability
- **VASP**: Requires proof of license
- **Intel Compilers**: Site license available
- **Commercial software**: Contact HPC support

If you have a license for commercial software, contact HPC support about installation.

## Frequently Asked Questions

### Why isn't my module loading?

- Check spelling: `module avail packagename`
- Module conflicts: Try `module purge` first
- Dependencies: Some modules require others to be loaded first

### How do I see which version of software is loaded?

```bash
$ module list
$ which python
$ python --version
```

### Can I use multiple versions of the same software?

Not simultaneously, but you can switch:
```bash
$ module unload python/3.10
$ module load python/3.11
```

### How do I make modules load automatically?

Add to your `~/.bashrc`:
```bash
module load python/3.11
```

```{warning}
Be cautious about loading modules automatically in `.bashrc`. This can cause issues with job scripts that need different module environments.
```

## Additional Resources

- [Anaconda](../software/anaconda.md)
- [Python and Jupyter Notebooks](../software/python_jupyter.md)
- [R](../software/r.md)
- [MATLAB](../software/matlab.md)
- [Using MPI with Fortran](../software/mpi_fortran.md)

## Questions?

For questions about available software or module usage, contact <hpc@nmthpc.atlassian.net>.
