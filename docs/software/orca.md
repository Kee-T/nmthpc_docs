# ORCA

This guide covers using ORCA for quantum chemistry calculations on NMTHPC.

## Loading ORCA

```bash
$ module avail orca
$ module load orca/6.1.1
```

## Running ORCA

### Testing ORCA

A sample ORCA job is available to verify that ORCA is functioning correctly on NMTHPC.

Copy the test archive to your home directory, extract it, navigate to the test directory, and submit the provided SLURM job.

[orca_test.tar.gz](https://github.com/user-attachments/files/30201358/orca_test.tar.gz)

```bash
$ tar -xzvf orca_test.tar.gz
$ cd orca_test
$ sbatch orca_test.sh
```

After submitting the job, you should receive output similar to:

```text
Submitted batch job <job_id>
```

This should allow you to run a job on the cluster for the first time on the NMTHPC system. 

## Contact

For questions about ORCA or assistance with running jobs on NMTHPC, contact <hpc@nmthpc.atlassian.net>.
