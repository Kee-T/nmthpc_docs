# Running Interactive Jobs

Interactive jobs allow you to work on compute nodes in real-time, making them ideal for testing, debugging, and development work.

## What are Interactive Jobs?

Interactive jobs provide:

- Direct command-line access to compute nodes
- Real-time feedback from your commands
- Ability to test and debug interactively
- Access to computational resources beyond login nodes

```{warning}
Never run computationally intensive work on login nodes. Always use interactive jobs (or batch jobs) to access compute resources.
```

## Basic Interactive Session

### Starting an Interactive Job

The simplest way to start an interactive job:

```bash
$ srun --pty bash
```

This requests:

- One task (CPU core)
- Default memory
- Default time limit
- A bash shell on a compute node

**Example session**:
```bash
[user@login01 ~]$ srun --pty bash
srun: job 12345 queued and waiting for resources
srun: job 12345 has been allocated resources
[user@node01 ~]$ # Now on compute node
[user@node01 ~]$ hostname
node01
[user@node01 ~]$ # Run your work here
[user@node01 ~]$ exit
[user@login01 ~]$ # Back to login node
```

### Specifying Resources

**Request specific resources**:
```bash
$ srun --ntasks=4 --mem=8G --time=02:00:00 --pty bash
```

**Common options**:

- `--ntasks=N` or `-n N`: Number of tasks (CPUs)
- `--mem=XG`: Memory in gigabytes
- `--time=HH:MM:SS`: Time limit
- `--partition=name`: Specific partition
- `--pty bash`: Interactive bash shell

## Common Interactive Job Examples

### General CPU Work

**Single-core interactive session**:
```bash
$ srun --ntasks=1 --mem=4G --time=01:00:00 --pty bash
```

**Multi-core for parallel testing**:
```bash
$ srun --ntasks=8 --mem=16G --time=02:00:00 --pty bash
```

### GPU Interactive Sessions

**Single GPU**:
```bash
$ srun --partition=gpu --gres=gpu:1 --mem=32G --time=04:00:00 --pty bash
```

**After allocation, verify GPU access**:
```bash
$ nvidia-smi
```

See [Running Jobs on GPU Nodes](gpu_jobs.md) for more GPU-specific information.

### High Memory Work

**Request large memory**:
```bash
$ srun --partition=cpu.hm --mem=256G --time=03:00:00 --pty bash
```

### Quick Testing (Testing Partition)

**Fast-start testing**:
```bash
$ srun --partition=testing --ntasks=2 --time=00:30:00 --pty bash
```

## Interactive Applications

### Python Interactive Session

```bash
$ srun --ntasks=1 --mem=8G --time=02:00:00 --pty bash
$ module load python/3.11
$ python
>>> import numpy as np
>>> # Interactive Python work
```

### Jupyter Notebooks

For Jupyter notebooks, see the section on Python and Jupyter notebooks for detailed setup instructions.

### R Interactive Session

```bash
$ srun --ntasks=1 --mem=16G --time=02:00:00 --pty bash
$ module load r/4.3.0
$ R
> # Interactive R work
```

See [R](../software/r.md) for more details.

### MATLAB Interactive Session

```bash
$ srun --ntasks=4 --mem=16G --time=04:00:00 --pty bash
$ module load matlab/R2023a
$ matlab -nodisplay -nosplash
>> # MATLAB commands
```

See [MATLAB](../software/matlab.md) for more information.

## Using X11 Forwarding for GUI Applications

### Setup X11 Forwarding

**When connecting to NMTHPC**:
```bash
$ ssh -X username@nmthpc.id.nmt.edu
```

or
```bash
$ ssh -Y username@nmthpc.id.nmt.edu  # Trusted X11 forwarding
```

**Start interactive job with X11**:
```bash
$ srun --x11 --pty bash
```

**Test X11**:
```bash
$ xclock  # Should show a clock window
```

### GUI Applications

**MATLAB with GUI**:
```bash
$ srun --x11 --ntasks=4 --mem=16G --time=04:00:00 --pty bash
$ module load matlab/R2023a
$ matlab  # Opens MATLAB GUI
```

**Visualization tools**:
```bash
$ srun --x11 --mem=16G --time=02:00:00 --pty bash
$ module load paraview
$ paraview  # Opens Paraview GUI
```



## Working in Interactive Sessions

**Monitor your resource usage**:
```bash
$ top -u $USER
$ free -h
```

**Extend time if needed**:

If your session is about to expire, save your work and start a new session. You cannot extend an active interactive job.

**Clean up**:
```bash
$ exit  # Always exit when done
```


## Troubleshooting

### Job Won't Start

**Check queue**:
```bash
$ squeue -u $USER
```

**Check why pending**:
```bash
$ squeue -u $USER -o "%.18i %.30j %.20R"
```

**Common reasons**:

- No resources available (wait)
- Requested resources exceed limits (reduce request)
- Partition down (try different partition)

### Session Disconnected

If your SSH connection drops, your interactive job is killed.

**Prevention**:

1. Use `tmux` or `screen`:
   ```bash
   $ tmux
   $ srun --pty bash
   # If disconnected, reconnect and: tmux attach
   ```

2. For long work, use batch jobs instead

### Out of Memory

If your program is killed:

```bash
$ dmesg | tail  # Check for OOM (Out of Memory) errors
```

**Solution**: Request more memory in next session
```bash
$ srun --mem=32G --pty bash  # Increased from 16G
```

### Time Limit Reached

**Warning before timeout**: Not provided by SLURM

**Solution**:

- Check remaining time: `squeue -u $USER`
- Request longer time initially
- Save work periodically
- For very long work, use batch jobs


## When to Use Interactive vs. Batch Jobs

### Use Interactive Jobs For:

- Testing and debugging code
- Developing workflows
- Short exploratory analyses
- Interactive data analysis
- Compiling software
- Quick computations (< 2 hours)

### Use Batch Jobs For:

- Production runs
- Long-running computations
- Jobs that don't need interaction
- Jobs you want to queue overnight/weekend
- Multiple similar jobs

See [Running Batch Jobs](batch_jobs.md) for batch job information.

## Example Workflows

### Testing Python Code

```bash
# Start interactive session
$ srun --ntasks=1 --mem=8G --time=01:00:00 --pty bash

# Load modules
$ module load python/3.11

# Test your code
$ python test_script.py

# Modify code based on results (use editor on login node in another terminal)

# Test again
$ python test_script.py

# Once working, exit and create batch script
$ exit
```

### GPU Development Workflow

```bash
# Request GPU interactively
$ srun --partition=gpu --gres=gpu:1 --mem=32G --time=02:00:00 --pty bash

# Load CUDA and frameworks
$ module load cuda/12.1
$ module load python/3.11

# Test GPU code
$ python gpu_test.py

# Check GPU usage
$ nvidia-smi

# Refine and test until working

# Exit and create batch script for full runs
$ exit
```

## Questions?

For questions about interactive jobs, contact <hpc@nmthpc.atlassian.net>.
