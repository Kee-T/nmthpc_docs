# New Mexico Tech High Performance Computing Documentation

Welcome to the New Mexico Tech High Performance Computing (NMTHPC) documentation. This guide provides comprehensive information about accessing, using, and optimizing your work on our HPC cluster.

## About NMTHPC

The NMT HPC cluster is a high-performance computing resource designed to support research and education at New Mexico Tech. Our system features:

- **{{nmthpc_total_cpu_nodes}}** CPU compute nodes for general-purpose computing
- **{{nmthpc_total_gpu_nodes}}** {{nmthpc_gpu_type}} GPU nodes for accelerated computing and AI/ML workloads
- Two high-performance filesystems: **{{nmthpc_filesystem_1}}** and **{{nmthpc_filesystem_2}}**
- SLURM job scheduler for efficient resource management

```{tip}
- New to HPC or NMTHPC? Start with our [Navigating the NMT HPC Documentation](./getting_started/navigating_docs.md) page
- Need help? Contact our support team at hpc-support@nmt.edu
- Looking for specific software? Check our [Software Available on NMTHPC](./computing_environment/software.md) page
```

----

::::{dropdown} Click to show the full index for all documentation
:icon: list-unordered

```{toctree}
:maxdepth: 1
:caption: Getting Started

getting_started/navigating_docs
getting_started/accounts_login
getting_started/faq
getting_started/acknowledging_nmthpc
```

```{toctree}
:maxdepth: 1
:caption: Computing Environment

computing_environment/nodes_filesystems
computing_environment/software
computing_environment/data_transfer
computing_environment/monitoring_resources
computing_environment/partitions_qos
```

```{toctree}
:maxdepth: 1
:caption: Using NMTHPC

using_nmthpc/interactive_jobs
using_nmthpc/batch_jobs
using_nmthpc/job_arrays
using_nmthpc/gpu_jobs
```

```{toctree}
:maxdepth: 1
:caption: Software and Examples

software/anaconda
software/python_jupyter
software/ai_ml_gpu
software/r
software/matlab
software/vasp
software/mpi_fortran
```

```{toctree}
:maxdepth: 1
:caption: Programming tutorials

programming/coding-best-practices
programming/MPI-C
programming/MPI-Fortran
programming/OpenMP-C
programming/OpenMP-Fortran
programming/parallel-programming-fundamentals
programming/profiling-nvidia-gpu-performance
```

::::
