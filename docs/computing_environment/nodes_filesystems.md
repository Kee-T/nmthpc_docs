# Nodes and Filesystems

This page provides information about the hardware architecture and storage systems available on NMTHPC.

## Cluster Overview

The NMT HPC cluster consists of:

- **{{nmthpc_total_cpu_nodes}}** CPU compute nodes for general-purpose computing
- **{{nmthpc_total_gpu_nodes}}** GPU nodes with {{nmthpc_gpu_type}} GPUs for accelerated workloads
- Multiple login nodes for user access
- Two high-performance filesystems: **{{nmthpc_filesystem_1}}** 1 (backed up in **{{nmthpc_filesystem_1}}** 2) and **{{nmthpc_filesystem_2}}**

## Node Types

### Login Nodes

Login nodes are your entry point to the cluster. When you SSH to NMTHPC, you connect to a login node.
Your home directory will be in the **{{nmthpc_filesystem_1}}** 1 filesystem, which is automatically backed up to **{{nmthpc_filesystem_1}}** 2. 

**Purpose**:

- File editing and management
- Code compilation
- Job submission and monitoring
- Small file transfers
- Viewing results

```{warning}
**Login nodes are shared resources.** Do not run computationally intensive tasks on login nodes. Use SLURM to submit jobs to compute nodes or interactive jobs via `srun` to compile software.
```

**Appropriate uses**:

- Editing scripts with vim or nano
- Compiling lightweight codes (single procesor, seconds)
- Starting interactive jobs with `srun` to compile or test codes
- Submitting jobs with `sbatch` or `srun`
- Checking job status with `squeue`
- Light data processing (single processor)

**Inappropriate uses**:

- Running simulations or large-scale analyses
- Training machine learning models
- Processing large datasets
- Compiling computationally intensive software packages
- Any task requiring significant CPU or memory

### CPU Compute Nodes

CPU compute nodes are designed for general-purpose parallel computing.

**Specifications** (typical):

- Processor: Multi-core CPUs
- Cores per node: 256 
- Memory: Varies by node type



**Accessing CPU nodes**:

Interactive:
```bash
$ srun --pty bash
```

Batch job:
```bash
$ sbatch cpu_job.sh
```

See [Running Interactive Jobs](../using_nmthpc/interactive_jobs.md) and [Running Batch Jobs](../using_nmthpc/batch_jobs.md) for details.

### GPU Compute Nodes

NMTHPC features {{nmthpc_total_gpu_nodes}} GPU nodes equipped with **{{nmthpc_gpu_type}}** GPUs.

**GPU Specifications**:

- GPU Model: NVIDIA **{{nmthpc_gpu_type}}**



**Requesting GPU resources**:

Interactive:
```bash
$ srun --gres=gpu:1 --pty bash
```

Batch job script:
```bash
#SBATCH --gres=gpu:1
#SBATCH --partition=gpu
```

See [Running Jobs on GPU Nodes](../using_nmthpc/gpu_jobs.md) for comprehensive guidance.

## Filesystems

NMTHPC provides multiple storage systems optimized for different use cases.

### Home Directory

**Path**: `/home/username`

**Characteristics**:

- Personal storage space
- Backed up (ZFS1 filesystem backed up in filesystem ZFS2)
- Limited quota
- Accessible from all nodes

**Best for**:

- Source code and scripts
- Configuration files
- Small datasets
- Job submission scripts

**Quota**: Check your usage with:
```bash
$ quota -s
```

```{tip}
Keep your home directory organized and clean. Regularly delete unnecessary files to stay within quota limits.
```

### {{nmthpc_filesystem_2}} Filesystem

This is a scratch file with no backup, periodically wiped. Do not store important data here!


**Path**: Under `/data/username` 


**Characteristics**:

- High-performance parallel filesystem
- Optimized for large-scale I/O
- Larger storage allocation
- Shared across compute nodes

**Best for**:

- Active project data
- Large datasets being actively processed
- Simulation input and output files
- High I/O workloads

This is a scratch space for temporary files needed during job execution.


**Characteristics**:

- Not backed up
- Periodically cleaned up 

**Best for**:

- Temporary data or model output
- Intermediate results
- Reducing I/O to shared filesystems

```{warning}
Data in local scratch `\data` is periodically deleted (e.g., every 90 days) and not backed up. Always copy important results to a permanent filesystem or to other machines.
```

## Storage Best Practices

### Choosing the Right Filesystem

| Use Case | Recommended Location |
|----------|---------------------|
| Scripts and code | Home directory |
| Small datasets  | Home directory |
| Long-term project storage | {{nmthpc_filesystem_1}} |
| Active large datasets | scratch {{nmthpc_filesystem_2}} |
| Temporary files during jobs | scratch {{nmthpc_filesystem_2}} |

### Managing Disk Quotas

Check your current usage:
```bash
$ quota -s
```

View disk usage by directory:
```bash
$ du -h --max-depth=1 ~/
```

Find large files:
```bash
$ find ~/ -type f -size +1G
```

### Data Organization Tips

1. **Use project directories**: Organize data by project or research topic
2. **Clean up regularly**: Delete intermediate files and failed job outputs
3. **Compress when possible**: Use `gzip`, `tar`, or other compression tools
4. **Archive completed projects**: Move finished projects to long-term storage

### File Permissions

Ensure appropriate file permissions:

```bash
# Make script executable
$ chmod +x script.sh

# Make directory readable by group
$ chmod g+r directory/

# Restrict file to owner only
$ chmod 600 sensitive_file
```

## Monitoring Resource Usage

### Check Node Information

See available nodes:
```bash
$ sinfo
```

View node details:
```bash
$ scontrol show nodes
```

### Check Your Job's Resource Usage

While job is running:
```bash
$ squeue -u $USER
```

After job completes:
```bash
$ sacct -j JOBID --format=JobID,JobName,Elapsed,MaxRSS,MaxVMSize,State
```

See [Monitoring Resources](monitoring_resources.md) for more detailed information.

## Hardware Specifications Summary

For detailed hardware specifications of specific node types and partitions, contact HPC support or see [Partitions and QOS](partitions_qos.md).

```{note}
Hardware configurations may change as the system is upgraded. Always check current specifications with `sinfo` or contact HPC support for the most up-to-date information.
```

## Questions?

For questions about node types, storage systems, or hardware specifications, contact HPC support at <hpc@nmthpc.atlassian.net>.
