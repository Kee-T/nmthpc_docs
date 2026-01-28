# Monitoring Resources

This guide covers tools and commands for monitoring your jobs, system resources, and resource usage on NMTHPC.

## Monitoring Your Jobs

### Viewing Job Queue

**See all your jobs**:
```bash
$ squeue -u $USER
```

**Output columns**:

- `JOBID`: Unique job identifier
- `PARTITION`: Queue/partition where job is running
- `NAME`: Job name
- `USER`: Your username
- `ST`: Job state (R=Running, PD=Pending, CG=Completing)
- `TIME`: Time job has been running
- `NODES`: Number of nodes allocated
- `NODELIST`: Which nodes are allocated

**See specific job**:
```bash
$ squeue -j JOBID
```

**See all jobs (all users)**:
```bash
$ squeue
```

**Customize output format**:
```bash
$ squeue -u $USER -o "%.18i %.9P %.8j %.8u %.2t %.10M %.6D %R"
```

### Job Status Codes

Common status codes in the `ST` column:

| Code | State | Meaning |
|------|-------|---------|
| PD | Pending | Job is waiting for resources |
| R | Running | Job is currently running |
| CG | Completing | Job is in the process of completing |
| CD | Completed | Job has completed successfully |
| F | Failed | Job terminated with non-zero exit code |
| TO | Timeout | Job reached time limit |
| OOM | Out of Memory | Job exceeded memory limit |

### Detailed Job Information

**Current job details**:
```bash
$ scontrol show job JOBID
```

This shows comprehensive information including:

- Requested resources
- Allocated nodes
- Time limits
- Working directory
- Job state reason

**Why is my job pending?**:
```bash
$ squeue -u $USER -o "%.18i %.9P %.30j %.8u %.2t %.10M %.10l %.6D %.20R"
```

The `REASON` column shows why a job is pending:

- `Resources`: Waiting for requested resources
- `Priority`: Other jobs have higher priority
- `QOSMaxCpuPerUserLimit`: You've hit your CPU limit
- `QOSMaxJobsPerUserLimit`: You've hit your job limit

### Job History and Accounting

**View completed jobs** (last 24 hours):
```bash
$ sacct
```

**Specific job details**:
```bash
$ sacct -j JOBID --format=JobID,JobName,Partition,State,Elapsed,MaxRSS,MaxVMSize
```

**Useful sacct formats**:
```bash
$ sacct -j JOBID --format=JobID,JobName,Start,End,Elapsed,State,ExitCode
$ sacct -j JOBID --format=JobID,MaxRSS,MaxVMSize,AveCPU,TotalCPU
```

**View jobs from specific date range**:
```bash
$ sacct --starttime=2024-01-01 --endtime=2024-01-31 -u $USER
```

**Format codes**:

- `MaxRSS`: Maximum memory used
- `MaxVMSize`: Maximum virtual memory
- `Elapsed`: Total runtime
- `TotalCPU`: Total CPU time used
- `State`: Final state of the job

## Real-Time Job Monitoring

### Monitoring Running Jobs

**SSH to the compute node** (while job is running):

First, find which node:
```bash
$ squeue -u $USER
```

Then connect:
```bash
$ ssh nodeXXX
```

```{warning}
Only SSH to nodes where you have an active job. Do not access nodes where you don't have a running job.
```

### Checking Resource Usage

**Once on the compute node**:

**CPU and memory usage**:
```bash
$ top
```

or for a better interface:
```bash
$ htop
```

**Your processes only**:
```bash
$ top -u $USER
```

**Memory usage**:
```bash
$ free -h
```

**Disk I/O**:
```bash
$ iostat -x 5
```

### GPU Monitoring

**Check GPU status**:
```bash
$ nvidia-smi
```

**Continuous monitoring** (updates every 2 seconds):
```bash
$ watch -n 2 nvidia-smi
```

**GPU utilization details**:
```bash
$ nvidia-smi --query-gpu=timestamp,gpu_name,utilization.gpu,utilization.memory,memory.total,memory.used,memory.free --format=csv
```

**Monitor specific process**:
```bash
$ nvidia-smi pmon
```

## System-Wide Monitoring

### Cluster Status

**View partition information**:
```bash
$ sinfo
```

**Output columns**:

- `PARTITION`: Queue name
- `AVAIL`: Partition availability
- `TIMELIMIT`: Maximum job time
- `NODES`: Number of nodes
- `STATE`: Node states
- `NODELIST`: List of nodes

**Detailed node information**:
```bash
$ sinfo -Nel
```

**Show only available nodes**:
```bash
$ sinfo -t idle
```

### Node Details

**Information about specific node**:
```bash
$ scontrol show node nodeXXX
```

**All nodes in partition**:
```bash
$ scontrol show partition partitionname
```

## Storage Monitoring

### Check Disk Quota

**Your quota usage**:
```bash
$ quota -s
```

**Detailed filesystem usage**:
```bash
$ df -h
```

### Disk Usage

**Home directory usage**:
```bash
$ du -sh ~/
```

**Usage by subdirectory**:
```bash
$ du -h --max-depth=1 ~/ | sort -h
```

**Find large files**:
```bash
$ find ~/ -type f -size +1G -exec ls -lh {} \;
```

**Largest files in directory**:
```bash
$ du -ah ~/ | sort -rh | head -20
```

## Job Output Files

### SLURM Output Files

By default, SLURM creates output files:

- `slurm-JOBID.out`: Combined stdout and stderr

**Custom output files** (in your job script):
```bash
#SBATCH --output=job_%j.out
#SBATCH --error=job_%j.err
```

**View output while job runs**:
```bash
$ tail -f slurm-JOBID.out
```

**Search output for errors**:
```bash
$ grep -i error slurm-JOBID.out
```

## Email Notifications

**Get email alerts** about job status:

Add to your SLURM script:
```bash
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=your.email@nmt.edu
```

**Mail types**:

- `BEGIN`: Job starts
- `END`: Job completes
- `FAIL`: Job fails
- `ALL`: All events

## Job Efficiency

### Analyzing Resource Usage

**After job completes**:
```bash
$ seff JOBID
```

This shows:

- CPU efficiency
- Memory efficiency
- Time used vs. requested

**Example output**:
```
Job ID: 12345
Cluster: nmthpc
User/Group: username/group
State: COMPLETED
Cores: 4
CPU Utilized: 03:45:22
CPU Efficiency: 93.84%
Memory Utilized: 12.5 GB
Memory Efficiency: 62.50%
```

### Improving Efficiency

Based on `seff` output:

**Low CPU efficiency**:

- Your code may not be parallelized properly
- You requested more cores than your code can use
- Reduce core count or improve parallelization

**Low memory efficiency**:

- You requested too much memory
- Reduce `--mem` in future jobs to save resources

**High memory usage**:

- Increase `--mem` to avoid out-of-memory errors
- Consider using high-memory nodes if needed

## Custom Monitoring Scripts

### Simple Status Check Script

**monitor_job.sh**:
```bash
#!/bin/bash
JOBID=$1

echo "Job Status:"
squeue -j $JOBID

echo -e "\nResource Usage:"
sacct -j $JOBID --format=JobID,JobName,Elapsed,State,MaxRSS,MaxVMSize

echo -e "\nOutput tail:"
if [ -f "slurm-${JOBID}.out" ]; then
    tail -20 slurm-${JOBID}.out
fi
```

**Usage**:
```bash
$ chmod +x monitor_job.sh
$ ./monitor_job.sh JOBID
```

### Watch Multiple Jobs

**watch_jobs.sh**:
```bash
#!/bin/bash
watch -n 10 "squeue -u $USER -o '%.10i %.12j %.8T %.10M %.4D %R'"
```

## Troubleshooting

### Job Not Starting

**Check why job is pending**:
```bash
$ squeue -u $USER -o "%.18i %.30j %.20R"
```

**Common reasons**:

- Insufficient resources available
- Requested more resources than partition has
- Hit job or resource limits
- Partition down for maintenance

### Job Killed Unexpectedly

**Check job status**:
```bash
$ sacct -j JOBID --format=JobID,State,ExitCode,DerivedExitCode
```

**Common causes**:

- `OUT_OF_MEMORY`: Requested insufficient memory
- `TIMEOUT`: Job exceeded time limit
- `FAILED`: Non-zero exit code
- `CANCELLED`: You or admin cancelled it

### High Memory Usage

**Identify memory-intensive jobs**:
```bash
$ sacct -S 2024-01-01 -u $USER --format=JobID,JobName,MaxRSS,State | grep -v "batch\|extern"
```

**Monitor memory in real-time**:

SSH to compute node and run:
```bash
$ watch -n 5 'ps aux --sort=-%mem | head -20'
```

## Best Practices

### Before Submitting Large Jobs

1. **Test with small jobs** first
2. **Check available resources**: `sinfo`
3. **Request appropriate resources** based on testing
4. **Set realistic time limits** with buffer

### During Job Execution

1. **Monitor initial progress**: Check job starts correctly
2. **Verify resource usage**: Ensure not wasting resources
3. **Watch for errors**: Check output files periodically

### After Job Completion

1. **Check efficiency**: Use `seff JOBID`
2. **Review output**: Look for errors or warnings
3. **Adjust future jobs**: Based on actual usage
4. **Clean up**: Remove unnecessary output files

## Useful Aliases

Add to your `~/.bashrc`:

```bash
# Job monitoring aliases
alias myq='squeue -u $USER'
alias myjobs='sacct --format=JobID,JobName,Partition,State,Elapsed,MaxRSS'
alias nodes='sinfo -Nel'
alias checkquota='quota -s'
```

Reload:
```bash
$ source ~/.bashrc
```

## Summary of Key Commands

| Task | Command |
|------|---------|
| View your jobs | `squeue -u $USER` |
| Job details | `scontrol show job JOBID` |
| Job history | `sacct -j JOBID` |
| Job efficiency | `seff JOBID` |
| GPU monitoring | `nvidia-smi` |
| Disk quota | `quota -s` |
| Cluster status | `sinfo` |
| Disk usage | `du -sh ~/` |

## Questions?

For questions about monitoring jobs or resource usage, contact <hpc-support@nmt.edu>.
