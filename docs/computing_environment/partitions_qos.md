# Partitions and Quality of Service (QOS)

This page explains the partition and Quality of Service (QOS) systems used on NMTHPC to manage access to computing resources.

## Overview

NMTHPC uses **partitions** and **QOS** (Quality of Service) policies to:

- Organize nodes by hardware type
- Prioritize different types of jobs
- Ensure fair resource sharing
- Manage job scheduling

## Partitions

Partitions are groups of nodes with similar characteristics. Think of them as different queues for different types of work.

### Viewing Available Partitions

```bash
$ sinfo
```

**Example output**:
```
PARTITION AVAIL  TIMELIMIT  NODES  STATE NODELIST
standard*    up 7-00:00:00     14   idle node[01-14]
standard*    up 7-00:00:00      2  alloc node[15-16]
gpu          up 2-00:00:00      1   idle gpu01
gpu          up 2-00:00:00      1  alloc gpu02
highmem      up 7-00:00:00      2   idle himem[01-02]
```

**Key columns**:

- `PARTITION`: Partition name (* indicates default)
- `AVAIL`: Availability status
- `TIMELIMIT`: Maximum job runtime
- `NODES`: Number of nodes
- `STATE`: Node state (idle, allocated, down, etc.)
- `NODELIST`: Which nodes are in this partition

### Common Partitions

```{note}
Partition names and configurations below are examples. Use `sinfo` to see actual partitions on NMTHPC.
```

#### Standard Partition

**Purpose**: General-purpose CPU computing

**Characteristics**:

- Default partition
- CPU compute nodes
- Standard memory allocation
- Typical time limit: 7 days

**When to use**:

- Standard computational jobs
- MPI parallel applications
- CPU-intensive workloads

**Example job submission**:
```bash
#SBATCH --partition=standard
#SBATCH --ntasks=16
#SBATCH --time=24:00:00
```

#### GPU Partition

**Purpose**: GPU-accelerated computing

**Characteristics**:

- Nodes with {{nmthpc_gpu_type}} GPUs
- Shorter time limits (to encourage turnover)
- Limited number of nodes (high demand)

**When to use**:

- Deep learning and AI/ML
- GPU-accelerated scientific computing
- CUDA applications

**Example job submission**:
```bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --time=48:00:00
```

See [Running Jobs on GPU Nodes](../using_nmthpc/gpu_jobs.md) for detailed guidance.

#### High Memory Partition

**Purpose**: Memory-intensive applications

**Characteristics**:

- Nodes with large RAM (typically > 256 GB)
- For applications that need more memory than standard nodes
- May have fewer cores per GB than standard nodes

**When to use**:

- Genome assembly
- Large-scale data analysis
- Applications with high memory requirements

**Example job submission**:
```bash
#SBATCH --partition=highmem
#SBATCH --mem=500G
#SBATCH --time=24:00:00
```

#### Debug/Test Partition

**Purpose**: Quick testing and development

**Characteristics**:

- Higher priority for fast job starts
- Short time limits (typically 1-4 hours)
- Limited resources

**When to use**:

- Testing job scripts
- Debugging code
- Short interactive sessions

**Example job submission**:
```bash
#SBATCH --partition=debug
#SBATCH --time=01:00:00
```

### Specifying Partitions

**In job script**:
```bash
#SBATCH --partition=gpu
```

**On command line**:
```bash
$ sbatch --partition=gpu myjob.sh
```

**Interactive job**:
```bash
$ srun --partition=debug --pty bash
```

**Omit for default partition**:
```bash
# Uses default partition if not specified
$ sbatch myjob.sh
```

## Quality of Service (QOS)

QOS policies control job priority, resource limits, and scheduling behavior.

### Viewing QOS Information

**List available QOS**:
```bash
$ sacctmgr show qos
```

**Your account's QOS**:
```bash
$ sacctmgr show user $USER withassoc format=user,account,qos
```

### Common QOS Levels

```{note}
QOS names and policies below are examples. Contact HPC support for actual QOS configuration on NMTHPC.
```

#### Normal QOS

**Characteristics**:

- Default QOS for most users
- Standard priority
- Reasonable resource limits
- Most jobs run under this QOS

**Limits** (examples):

- Max jobs per user: 100
- Max cores per user: 128
- Max GPUs per user: 2
- Max wall time: 7 days

#### High Priority QOS

**Characteristics**:

- Higher scheduling priority
- For time-sensitive work
- May require special request

**When to use**:

- Conference deadlines
- Time-critical research
- Approved special projects

**Request**: Contact HPC support

#### Long QOS

**Characteristics**:

- Extended time limits
- Lower priority
- For jobs that truly need extended runtime

**When to use**:

- Simulations requiring > 7 days
- Long-running optimizations

**Example**:
```bash
#SBATCH --qos=long
#SBATCH --time=14-00:00:00
```

### Specifying QOS

**In job script**:
```bash
#SBATCH --qos=normal
```

**On command line**:
```bash
$ sbatch --qos=long myjob.sh
```

## Resource Limits

### Partition Limits

Each partition has limits on:

**Time limits**: Maximum wall time for jobs
```bash
$ sinfo -o "%P %.11l"  # Show partition time limits
```

**Node limits**: Maximum nodes per job

**GPU limits**: Maximum GPUs per user or job

### QOS Limits

QOS policies may limit:

- **Max jobs per user**: How many jobs you can have queued/running
- **Max CPUs per user**: Total CPUs across all your jobs
- **Max GPUs per user**: Total GPUs across all your jobs
- **Max wall time**: Longest allowed job duration
- **Max submit jobs**: How many jobs you can submit

### Checking Your Limits

**View your current usage**:
```bash
$ squeue -u $USER
```

**Count your running jobs**:
```bash
$ squeue -u $USER -t RUNNING | wc -l
```

**Total CPUs in use**:
```bash
$ squeue -u $USER -t RUNNING -o "%C" | tail -n +2 | awk '{sum+=$1} END {print sum}'
```

## Job Priority

Job priority determines the order in which pending jobs start when resources become available.

### Priority Factors

**Factors affecting priority**:

1. **QOS**: Higher QOS = higher priority
2. **Fair share**: Users with less recent usage get higher priority
3. **Job age**: Older pending jobs get priority boost
4. **Job size**: Smaller jobs may get priority to fill gaps
5. **Partition**: Some partitions have priority policies

### Viewing Job Priority

```bash
$ sprio
```

or for your jobs only:
```bash
$ sprio -u $USER
```

**Output columns**:

- `JOBID`: Job identifier
- `PRIORITY`: Overall priority score
- `AGE`: Priority from wait time
- `FAIRSHARE`: Priority from fair-share algorithm
- `QOS`: Priority from QOS

Higher numbers = higher priority

## Fair Share

NMTHPC uses fair-share scheduling to ensure equitable resource distribution.

### How Fair Share Works

- Tracks your recent resource usage
- Users with less recent usage get higher priority
- Encourages balanced resource sharing
- Usage "decays" over time (typically ~2 weeks)

### Checking Fair Share

```bash
$ sshare -u $USER
```

**Key fields**:

- `FairShare`: Your current fair-share factor (0.0-1.0)
- `Usage`: Your recent usage
- Higher FairShare = higher job priority

```{tip}
If your jobs are pending and you have high recent usage, your fair-share priority may be low. Other users with less recent usage will get priority. Wait times typically improve as your usage "decays."
```

## Best Practices

### Choosing the Right Partition

1. **Match hardware to needs**:
   - GPUs needed → GPU partition
   - High memory needed → High memory partition
   - Standard CPU work → Standard partition

2. **Consider time limits**:
   - Short jobs → Debug/test partition
   - Standard jobs → Standard partition
   - Very long jobs → Long QOS or special request

3. **Test first**:
   - Use debug partition for initial testing
   - Scale up to production partitions

### Optimizing Job Priority

1. **Request only what you need**:
   - Don't request excessive time or resources
   - Smaller resource requests = faster starts

2. **Be strategic with submissions**:
   - Submit jobs when you're ready to use results
   - Don't queue hundreds of jobs unless necessary

3. **Use appropriate QOS**:
   - Normal QOS for routine work
   - Special QOS only when truly needed

### Resource Request Strategy

```{warning}
Requesting more resources than you need:
- Wastes cluster resources
- Reduces your fair-share priority
- Makes jobs take longer to start
- Decreases efficiency metrics
```

**Do request**:

- Actual time needed + 20% buffer
- Memory based on test runs
- Cores your code can actually use

**Don't request**:

- Maximum time "just in case"
- All available memory "to be safe"
- All cores on a node if you'll use only a few

## Troubleshooting

### Job Won't Start

**Check partition availability**:
```bash
$ sinfo -p partitionname
```

**Check QOS limits**:
```bash
$ sacctmgr show qos format=Name,MaxWall,MaxTRES
```

**View pending reason**:
```bash
$ squeue -u $USER -o "%.18i %.30j %.20R"
```

### Hit Resource Limits

**Common limit messages**:

- `QOSMaxCpuPerUserLimit`: You're using max CPUs allowed
- `QOSMaxJobsPerUserLimit`: You have max jobs queued
- `QOSMaxGRESPerUser`: You're using max GPUs allowed

**Solutions**:

- Wait for running jobs to complete
- Cancel unnecessary jobs
- Request different QOS if appropriate
- Contact HPC support for special needs

### Job Priority Too Low

**Check fair-share**:
```bash
$ sshare -u $USER
```

**Check priority**:
```bash
$ sprio -u $USER
```

**Improve priority**:

- Wait for usage to decay
- Request smaller resource allocations
- Use appropriate QOS
- Submit fewer concurrent jobs

## Getting More Information

**Partition details**:
```bash
$ scontrol show partition partitionname
```

**QOS details**:
```bash
$ sacctmgr show qos qosname format=Name,Priority,MaxWall,MaxTRES
```

**Your account details**:
```bash
$ sacctmgr show user $USER withassoc format=user,account,partition,qos,defaultqos
```

## Questions?

For questions about partitions, QOS policies, or resource limits, contact <hpc@nmthpc.atlassian.net>.

For special resource requests or custom QOS, include:

- Why you need special resources
- How long you'll need them
- Estimated resource requirements
- Project timeline
