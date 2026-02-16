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
$ srun --partition=highmem --mem=256G --time=03:00:00 --pty bash
```

### Quick Testing (Debug Partition)

**Fast-start testing**:
```bash
$ srun --partition=debug --ntasks=2 --time=00:30:00 --pty bash
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

For Jupyter notebooks, see [Python and Jupyter Notebooks](../software/python_jupyter.md) for detailed setup instructions.

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
$ ssh -X username@hpc.nmt.edu
```

or
```bash
$ ssh -Y username@hpc.nmt.edu  # Trusted X11 forwarding
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

```{note}
X11 forwarding over network can be slow. For intensive visualization, consider using VNC or web-based tools.
```

## Working in Interactive Sessions

### Best Practices

**1. Monitor your resource usage**:
```bash
$ top -u $USER
$ free -h
```

**2. Work efficiently**:

- Plan your work before starting the session
- Keep notes of successful commands for batch scripts
- Don't leave sessions idle

**3. Extend time if needed**:

If your session is about to expire, save your work and start a new session. You cannot extend an active interactive job.

**4. Clean up**:
```bash
$ exit  # Always exit when done
```

### Transferring Data During Interactive Sessions

**From login node to compute node**:

Files on shared filesystems (home, project directories) are accessible on compute nodes. No transfer needed.

**From local machine**:

Open another terminal and use scp/rsync to transfer to your home directory:
```bash
$ scp file.dat username@hpc.nmt.edu:~/
```

### Saving Your Interactive Work

**Command history**:
```bash
$ history > commands.txt  # Save commands for later
```

**Create batch script from interactive commands**:

Once you've tested interactively, create a batch script:

```bash
#!/bin/bash
#SBATCH --ntasks=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00

module load python/3.11

# Commands you tested interactively
python my_script.py
```

See [Running Batch Jobs](batch_jobs.md) for more on batch job scripts.

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

## Advanced Interactive Usage

### Running MPI Programs Interactively

```bash
$ srun --ntasks=8 --pty bash
$ module load openmpi/4.1.4
$ mpirun -np 8 ./my_mpi_program
```

### Multiple Interactive Jobs

You can have multiple interactive jobs simultaneously:

**Terminal 1**:
```bash
$ srun --ntasks=4 --mem=8G --pty bash
```

**Terminal 2** (in another SSH session):
```bash
$ srun --partition=gpu --gres=gpu:1 --mem=16G --pty bash
```

Check all your jobs:
```bash
$ squeue -u $USER
```

### Using Job Arrays Interactively

Not recommended. Job arrays are designed for batch work. See [Using SLURM Job Arrays](job_arrays.md).

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

## Summary

**Quick reference for interactive jobs**:

| Task | Command |
|------|---------|
| Basic session | `srun --pty bash` |
| With resources | `srun --ntasks=4 --mem=16G --time=02:00:00 --pty bash` |
| GPU session | `srun --partition=gpu --gres=gpu:1 --pty bash` |
| With X11 | `srun --x11 --pty bash` |
| Check your jobs | `squeue -u $USER` |
| Exit session | `exit` |

## Questions?

For questions about interactive jobs, contact <hpc@nmthpc.atlassian.net>.
