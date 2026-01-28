# Frequently Asked Questions

This page answers common questions about using the NMT HPC cluster.

## Account and Access

### How do I get an account on NMTHPC?

See our [Accounts and System Login](accounts_login.md) page for detailed instructions on requesting an account.

### I forgot my password. How do I reset it?

Contact the HPC support team at <hpc-support@nmt.edu> to request a password reset. Include your username in the request.

### Can I access NMTHPC from off campus?

Yes, but you'll need to connect through the NMT VPN first. Contact NMT IT Services for VPN access and configuration instructions.

### How long do NMTHPC accounts remain active?

Student accounts are reviewed annually. Faculty and staff accounts remain active as long as you're affiliated with NMT. Inactive accounts may be deactivated after extended periods of non-use.

## Storage and Data

### Where should I store my files?

NMTHPC has two main filesystems:

- **Home directory** (\`/home/username\`): For personal files, scripts, and configuration. Limited quota.
- **{{nmthpc_filesystem_1}}**: High-performance filesystem for active project data
- **{{nmthpc_filesystem_2}}**: Additional storage filesystem for larger datasets

See [Nodes and Filesystems](../computing_environment/nodes_filesystems.md) for more details.

### What are the storage quotas?

Storage quotas vary by filesystem. Check your current usage with:

\`\`\`bash
$ quota -s
\`\`\`

Contact HPC support if you need additional storage space.

### How do I transfer data to NMTHPC?

Common methods include:

- \`scp\` for small to medium files
- \`rsync\` for synchronizing directories
- \`sftp\` for interactive transfers
- Globus for large datasets

See [Transferring Data](../computing_environment/data_transfer.md) for detailed instructions.

### How do I back up my data?

NMTHPC filesystems are not automatically backed up. You're responsible for backing up important data to other locations. Consider:

- Copying critical data to your local machine
- Using institutional storage services
- Implementing version control (Git) for code

## Running Jobs

### What's the difference between login nodes and compute nodes?

**Login nodes** are for:

- Editing files
- Compiling code
- Submitting jobs
- Managing files

**Compute nodes** are for:

- Running simulations
- Data analysis
- Any computationally intensive work

Never run heavy computations on login nodes. Use SLURM to submit jobs to compute nodes.

### How do I run a job?

There are two main ways:

1. **Interactive jobs**: For testing and development
   \`\`\`bash
   $ srun --pty bash
   \`\`\`
   See [Running Interactive Jobs](../using_nmthpc/interactive_jobs.md)

2. **Batch jobs**: For production runs
   \`\`\`bash
   $ sbatch myjob.sh
   \`\`\`
   See [Running Batch Jobs](../using_nmthpc/batch_jobs.md)

### How do I check the status of my job?

\`\`\`bash
$ squeue -u $USER
\`\`\`

For more detailed information:

\`\`\`bash
$ scontrol show job JOBID
\`\`\`

See [Monitoring Resources](../computing_environment/monitoring_resources.md) for more commands.

### Why is my job pending?

Common reasons include:

- **Resources**: The requested resources (CPUs, GPUs, memory) aren't currently available
- **Priority**: Other jobs have higher priority
- **Limits**: You've reached your maximum number of running jobs
- **QOS**: Quality of Service restrictions

Check with:

\`\`\`bash
$ squeue -u $USER
\`\`\`

The \`REASON\` column shows why a job is pending.

### How do I cancel a job?

\`\`\`bash
$ scancel JOBID
\`\`\`

To cancel all your jobs:

\`\`\`bash
$ scancel -u $USER
\`\`\`

### My job failed. How do I find out why?

1. Check the SLURM output file (usually \`slurm-JOBID.out\`)
2. Review your job script for errors
3. Check resource limits (memory, time)
4. Look for error messages in your application's log files

If you need help debugging, contact HPC support with your job ID.

## Software

### What software is available on NMTHPC?

Use the \`module\` system to see available software:

\`\`\`bash
$ module avail
\`\`\`

See [Software Available on NMTHPC](../computing_environment/software.md) for a comprehensive list.

### How do I load software?

\`\`\`bash
$ module load softwarename
\`\`\`

Example:

\`\`\`bash
$ module load python/3.11
\`\`\`

### Can I install my own software?

Yes! You can:

- Install Python packages in your home directory with \`pip install --user\`
- Create Anaconda environments
- Compile software in your home directory
- Use containers (Singularity/Apptainer)

See specific software guides in the [Software and Examples](../software/anaconda.md) section.

### I need software that's not installed. What should I do?

Contact HPC support at <hpc-support@nmt.edu> with:

- Software name and version
- Why you need it
- Link to the software website

We'll evaluate requests for system-wide installation.

## GPU Computing

### How do I request a GPU for my job?

Use the \`--gres\` flag:

\`\`\`bash
$ srun --gres=gpu:1 --pty bash
\`\`\`

For batch jobs, add to your SLURM script:

\`\`\`bash
#SBATCH --gres=gpu:1
\`\`\`

See [Running Jobs on GPU Nodes](../using_nmthpc/gpu_jobs.md) for more details.

### How do I check if my job is using the GPU?

While your job is running on a GPU node:

\`\`\`bash
$ nvidia-smi
\`\`\`

This shows GPU utilization, memory usage, and running processes.

### Which GPU libraries are available?

NMTHPC provides:

- CUDA toolkit
- cuDNN for deep learning
- TensorFlow and PyTorch with GPU support
- NVIDIA HPC SDK

See [Software Available on NMTHPC](../computing_environment/software.md) for versions.

## Best Practices

### How can I be a good NMTHPC citizen?

- Don't run jobs on login nodes
- Request only the resources you need
- Test with short jobs before submitting long runs
- Clean up old data you no longer need
- Monitor your jobs and cancel failed ones
- Acknowledge NMTHPC in publications

### How should I structure my workflow?

1. **Develop and test** on your local machine when possible
2. **Transfer** only necessary data to NMTHPC
3. **Test** with small jobs or interactive sessions
4. **Scale up** to full production runs
5. **Transfer** results back to your local machine
6. **Clean up** intermediate files

### What are some common mistakes to avoid?

- Running computations on login nodes
- Not specifying enough memory or time
- Hard-coding paths instead of using variables
- Not checking job status after submission
- Ignoring error messages
- Requesting more resources than needed

## Getting Help

### How do I contact HPC support?

Email: <hpc-support@nmt.edu>

Include in your request:

- Detailed description of the issue
- Job IDs (if applicable)
- Error messages
- What you've already tried

### What information should I include in a support request?

- **For job issues**: Job ID, error messages, SLURM script
- **For software issues**: Software name, version, exact commands you ran
- **For login issues**: Error messages, your operating system
- **For data transfer issues**: Transfer method, file sizes, error messages

### How quickly will I get a response?

We aim to respond to all requests within 1-2 business days. Urgent issues may receive faster attention.

## Additional Questions?

If your question isn't answered here, please:

1. Search the full documentation using your browser's search function
2. Check the relevant section of the documentation
3. Contact HPC support at <hpc-support@nmt.edu>
