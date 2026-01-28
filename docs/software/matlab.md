# MATLAB

This guide covers using MATLAB on NMTHPC for numerical computing and data analysis.

## Loading MATLAB

```bash
$ module avail matlab
$ module load matlab/R2023a
```

## Running MATLAB

### Interactive MATLAB (No Display)

**On compute node**:
```bash
$ srun --cpus-per-task=4 --mem=16G --time=02:00:00 --pty bash
$ module load matlab/R2023a
$ matlab -nodisplay -nosplash
```

### With GUI (X11)

**Connect with X11 forwarding**:
```bash
$ ssh -X username@hpc.nmt.edu
$ srun --x11 --mem=16G --time=02:00:00 --pty bash
$ module load matlab/R2023a
$ matlab
```

### Running MATLAB Scripts

**Non-interactive execution**:
```bash
$ matlab -nodisplay -nosplash -r "script_name; exit"
```

**With input file** (`run_matlab.m`):
```matlab
% Your MATLAB code
data = rand(1000, 1000);
result = mean(data);
save('results.mat', 'result');
```

**Run**:
```bash
$ matlab -nodisplay -nosplash -r "run run_matlab; exit"
```

## Batch MATLAB Jobs

**SLURM script** (`matlab_job.sh`):
```bash
#!/bin/bash
#SBATCH --job-name=matlab_job
#SBATCH --output=matlab_%j.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=08:00:00

module load matlab/R2023a

matlab -nodisplay -nosplash -r "my_script; exit"
```

## Parallel MATLAB

### Parallel Computing Toolbox

**In MATLAB script**:
```matlab
% Create parallel pool
num_workers = str2num(getenv('SLURM_CPUS_PER_TASK'));
parpool('local', num_workers);

% Parallel for loop
parfor i = 1:100
    result(i) = expensive_computation(i);
end

% Close pool
delete(gcp);
```

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G

module load matlab/R2023a
matlab -nodisplay -nosplash -r "parallel_script; exit"
```

## GPU Computing with MATLAB

**GPU-accelerated computation**:
```matlab
% Create GPU array
A = gpuArray(rand(10000));
B = gpuArray(rand(10000));

% Computation on GPU
C = A * B;

% Transfer back to CPU
C_cpu = gather(C);
```

**SLURM script for GPU**:
```bash
#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32G

module load matlab/R2023a
matlab -nodisplay -nosplash -r "gpu_script; exit"
```

## Common MATLAB Patterns

### Save and Load Data

```matlab
% Save data
data = rand(100, 100);
save('mydata.mat', 'data');

% Load data
load('mydata.mat');
```

### Function Files

**Create function** (`my_function.m`):
```matlab
function result = my_function(x, y)
    % Function documentation
    result = x^2 + y^2;
end
```

### Command-Line Arguments

**MATLAB script accepting arguments**:
```matlab
function process_data(input_file, output_file)
    data = readmatrix(input_file);
    result = mean(data, 2);
    writematrix(result, output_file);
end
```

**Call from command line**:
```bash
$ matlab -nodisplay -nosplash -r "process_data('input.csv', 'output.csv'); exit"
```

## Best Practices

1. **Exit MATLAB explicitly**: Always use `exit` in batch scripts
2. **Suppress display**: Use `-nodisplay -nosplash` for batch jobs
3. **Parallel pool**: Match workers to `--cpus-per-task`
4. **Memory**: Request sufficient memory for your arrays
5. **Save regularly**: Save intermediate results

## Questions?

Contact <hpc-support@nmt.edu> for MATLAB support.
