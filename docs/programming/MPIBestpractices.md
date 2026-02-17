# MPI Best practices

This tutorial is adapted from the  CU Boulder Research Computing documentation, which is also licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/">Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License</a>.

<a rel="license" href="http://creativecommons.org/licenses/by-nc-nd/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-nd/4.0/88x31.png" /></a>


MPI, or Message Passing Interface, is a powerful library standard that allows for the parallel execution of applications across multiple processors on a system. It differs from other parallel execution libraries like OpenMP by also allowing a user to run their applications across multiple nodes. Unfortunately it can sometimes be a bit tricky to run a compiled MPI application within an HPC resource. The following page outlines best practices in running your MPI applications.  

```{attention}
Please note that this page *does not* cover compiling or optimization of MPI applications.  
```

## MPI Compatible Compilers and Libraries

### Selecting your Compiler and MPI

Multiple families of compilers are available to users, such as Intel and GCC.  Intel compilers have Intel MPI available for messsage passing, and GCC compilers have OpenMPI available for message passing. To load a compiler/MPI combo run one the following commands from a job script or compile node (note that you should subsitute the version you need for `<version>` in the examples below; available compiler versions can be seen by typing `module avail`):


(tabset-ref-mpi-best-compiler)=
`````{tab-set}
:sync-group: tabset-mpi-best-compiler

````{tab-item} Intel
:sync: mpi-best-compiler-intel

```bash
module load intel/<version> impi
```

````

````{tab-item} GCC
:sync: mpi-best-compiler-gcc

```bash
module load gcc/<version> openmpi

# Uncomment this additional line when adding this command to a JobScript!
# SLURM_EXPORT_ENV=ALL
```

````

````{tab-item} AOCC
:sync: mpi-best-compiler-aocc

```bash
module load aocc/<version> openmpi

# Uncomment this additional line when adding this command to a JobScript!
# SLURM_EXPORT_ENV=ALL
```

````

`````

```{important}
It is important to note that use of OpenMPI should be paired with the `SLURM_EXPORT_ENV=ALL` environment variable to ensure the job can function when scheduled from a login node!
```


## Commands to Run MPI Applications
Regardless of compiler or MPI distribution, there are 3 “wrapper” commands that will run MPI applications: `mpirun`, `mpiexec`, and `srun`. These “wrapper” commands should be used after loading in your desired compiler and MPI distribution and simply prepend whatever application you wish to run. Each command offers their own pros and cons alongside nuance as to how they function.


(tabset-ref-mpi-best-prac-run)=
`````{tab-set}
:sync-group: tabset-mpi-best-prac-run

````{tab-item} mpirun
:sync: mpi-best-prac-run-mpirun

`mpirun` is probably the most direct method to run MPI applications with the command being tied to the distribution. This means distribution dependent flags can be passed directly through the command.   

```bash
mpirun -np <core-count> ./<your-application>
```

````

````{tab-item} mpiexec
:sync: mpi-best-prac-run-mpiexec

`mpiexec` is a standardized MPI command execution command that allows for more general MPI flags to be passed. This means that commands are universal across all distributions.

```bash
mpiexec -np <core-count> ./<your-application>
```

````

````{tab-item} srun
:sync: mpi-best-prac-run-srun

The final command `srun` is probably the most abstracted away from a specific implementation. This command lets Slurm figure out specific MPI features that are available in your environment and handles running the process as a job. This command is usually a little less efficient and may have some issues with reliability. 

```bash
srun -n <core-count> ./<your-application>
```

````
`````

```{note}
RC usually recommends `mpirun` and `mpiexec` for simplicity and reliability when running MPI applications. `srun` should be used sparingly to avoid issues with execution.
```

## Running MPI 

Simply select the Compiler and MPI wrapper you wish to use and place it in a job script. In the following example, we run a 128 core, 4 hour job with a gcc compiler and OpenMPI:  

```
#!/bin/bash
#SBATCH --nodes=2
#SBATCH --time=04:00:00
#SBATCH --partition=cpu.std
#SBATCH --qos=normal
#SBATCH --constraint=ib
#SBATCH --ntasks=128
#SBATCH --job-name=mpi-job
#SBATCH --output=mpi-job.%j.out

module purge
module load gcc/10.3 openmpi
  
export SLURM_EXPORT_ENV=ALL

#Run a 128 core job across 2 nodes:
mpirun -np $SLURM_NTASKS /path/to/mycode.exe

#Note: $SLURM_NTASKS has a value of the amount of cores you requested
```

