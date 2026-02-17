# Using SLURM Job Arrays

Job arrays allow you to submit and manage large numbers of similar jobs efficiently. This guide covers how to use SLURM job arrays effectively.

## What are Job Arrays?

Job arrays let you submit many similar jobs with a single script:

**Benefits**:

- Submit hundreds or thousands of jobs with one command
- Each job gets a unique task ID
- Easier to manage than individual jobs
- More efficient than submitting jobs one-by-one

**Use cases**:

- Parameter sweeps
- Processing multiple input files
- Monte Carlo simulations
- Batch processing datasets
- Sensitivity analyses

## Basic Job Array

### Simple Example

Create a file named `array_job.sh`:

```bash
#!/bin/bash
#SBATCH --job-name=my_array
#SBATCH --output=output_%A_%a.txt
#SBATCH --array=1-10
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

echo "This is array task $SLURM_ARRAY_TASK_ID"
echo "Array job ID: $SLURM_ARRAY_JOB_ID"

# Your work here
sleep 10
echo "Task $SLURM_ARRAY_TASK_ID completed"
```

### Submit the Array

```bash
$ sbatch array_job.sh
Submitted batch job 12345
```

This creates 10 individual jobs (tasks 1-10), each with a unique task ID.

### Check Array Jobs

```bash
$ squeue -u $USER
```

Output shows:
```
JOBID    PARTITION  NAME       USER   ST  TIME  NODES NODELIST
12345_1  standard   my_array   user   R   0:05  1     node01
12345_2  standard   my_array   user   R   0:05  1     node02
12345_3  standard   my_array   user   PD  0:00  1     (Resources)
...
```

## Array Specification

### Array Ranges

**Sequential range**:
```bash
#SBATCH --array=1-100        # Tasks 1 through 100
```

**With step size**:
```bash
#SBATCH --array=1-100:2      # Tasks 1,3,5,...,99
#SBATCH --array=0-50:5       # Tasks 0,5,10,...,50
```

**Specific values**:
```bash
#SBATCH --array=1,5,10,15    # Only these specific tasks
```

**Combined**:
```bash
#SBATCH --array=1-10,15,20,25-30  # Multiple ranges and values
```

### Limiting Concurrent Tasks

Limit how many tasks run simultaneously:

```bash
#SBATCH --array=1-1000%20    # Run max 20 tasks at a time
```

This submits 1000 tasks but only runs 20 concurrently.

```{tip}
Use `%` to limit concurrent tasks when submitting very large arrays. This prevents overwhelming the scheduler and shares resources fairly.
```

## Array Environment Variables

SLURM provides special variables for array jobs:

```bash
$SLURM_ARRAY_JOB_ID       # Main job ID (same for all tasks)
$SLURM_ARRAY_TASK_ID      # Unique task ID within array
$SLURM_ARRAY_TASK_COUNT   # Total number of tasks
$SLURM_ARRAY_TASK_MIN     # First task ID
$SLURM_ARRAY_TASK_MAX     # Last task ID
```

## Output Files

### Using Array Variables in Filenames

**In SLURM directives**:

- `%A` = array job ID
- `%a` = array task ID
- `%j` = job ID (includes task ID for arrays)

**Example**:
```bash
#SBATCH --output=logs/job_%A_task_%a.out
#SBATCH --error=logs/job_%A_task_%a.err
```

For array job 12345, this creates:
```
logs/job_12345_task_1.out
logs/job_12345_task_2.out
...
```

## Practical Examples

### Processing Multiple Files

**Scenario**: Process 100 data files named `data_001.txt` through `data_100.txt`

```bash
#!/bin/bash
#SBATCH --job-name=process_files
#SBATCH --output=logs/process_%A_%a.out
#SBATCH --array=1-100
#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00

module load python/3.11

# Create input filename with zero-padding
INPUT_FILE=$(printf "data_%03d.txt" $SLURM_ARRAY_TASK_ID)
OUTPUT_FILE=$(printf "results_%03d.txt" $SLURM_ARRAY_TASK_ID)

# Process the file
python process.py --input $INPUT_FILE --output $OUTPUT_FILE

echo "Processed $INPUT_FILE"
```

### Using a File List

**Scenario**: Process files listed in a text file

**File list** (`files.txt`):
```
/data/sample_A.dat
/data/sample_B.dat
/data/sample_C.dat
...
```

**Job script**:
```bash
#!/bin/bash
#SBATCH --job-name=process_list
#SBATCH --output=logs/job_%A_%a.out
#SBATCH --array=1-100
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=01:00:00

module load python/3.11

# Get the filename from line number equal to task ID
INPUT_FILE=$(sed -n "${SLURM_ARRAY_TASK_ID}p" files.txt)

# Process the file
python analyze.py $INPUT_FILE

echo "Processed $INPUT_FILE"
```

### Parameter Sweep

**Scenario**: Test different parameter combinations

```bash
#!/bin/bash
#SBATCH --job-name=param_sweep
#SBATCH --output=logs/sweep_%A_%a.out
#SBATCH --array=1-27
#SBATCH --ntasks=1
#SBATCH --mem=8G
#SBATCH --time=04:00:00

module load python/3.11

# Define parameter arrays
ALPHAS=(0.1 0.5 1.0)
BETAS=(1.0 10.0 100.0)
GAMMAS=(0.01 0.1 1.0)

# Calculate indices (3x3x3 = 27 combinations)
NUM_BETA=3
NUM_GAMMA=3

IDX=$((SLURM_ARRAY_TASK_ID - 1))
ALPHA_IDX=$((IDX / (NUM_BETA * NUM_GAMMA)))
BETA_IDX=$(((IDX / NUM_GAMMA) % NUM_BETA))
GAMMA_IDX=$((IDX % NUM_GAMMA))

ALPHA=${ALPHAS[$ALPHA_IDX]}
BETA=${BETAS[$BETA_IDX]}
GAMMA=${GAMMAS[$GAMMA_IDX]}

echo "Running with alpha=$ALPHA, beta=$BETA, gamma=$GAMMA"

# Run simulation with these parameters
python simulate.py --alpha $ALPHA --beta $BETA --gamma $GAMMA \
    --output results_${ALPHA}_${BETA}_${GAMMA}.dat
```

### Monte Carlo Simulations

**Scenario**: Run 1000 independent simulations with different random seeds

```bash
#!/bin/bash
#SBATCH --job-name=monte_carlo
#SBATCH --output=logs/mc_%A_%a.out
#SBATCH --array=1-1000%50      # Max 50 concurrent
#SBATCH --ntasks=1
#SBATCH --mem=4G
#SBATCH --time=02:00:00

module load python/3.11

# Use task ID as random seed
SEED=$SLURM_ARRAY_TASK_ID

# Run simulation
python monte_carlo.py --seed $SEED --output mc_$SEED.dat

echo "Simulation $SEED completed"
```

### GPU Array Jobs

**Scenario**: Train multiple models on GPUs

```bash
#!/bin/bash
#SBATCH --job-name=train_models
#SBATCH --output=logs/train_%A_%a.out
#SBATCH --array=1-10
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --mem=32G
#SBATCH --time=12:00:00

module load cuda/12.1
module load python/3.11

# Each task trains a different model configuration
CONFIG_FILE="config_${SLURM_ARRAY_TASK_ID}.yaml"

# Train model
python train.py --config $CONFIG_FILE --gpu 0 \
    --output models/model_$SLURM_ARRAY_TASK_ID.pth

echo "Model $SLURM_ARRAY_TASK_ID trained"
```

See [Running Jobs on GPU Nodes](gpu_jobs.md) for more GPU information.

## Managing Array Jobs

### Viewing Array Jobs

**All your array tasks**:
```bash
$ squeue -u $USER
```

**Specific array job**:
```bash
$ squeue -j 12345
```

**Summary view**:
```bash
$ squeue -u $USER -r  # -r shows array tasks as ranges
```

### Canceling Array Jobs

**Cancel entire array**:
```bash
$ scancel 12345
```

**Cancel specific task**:
```bash
$ scancel 12345_5  # Cancel only task 5
```

**Cancel range of tasks**:
```bash
$ scancel 12345_[10-20]  # Cancel tasks 10-20
```

### Array Job Status

**Check completion**:
```bash
$ sacct -j 12345
```

**Summary of task states**:
```bash
$ sacct -j 12345 --format=JobID,State | grep -c COMPLETED
$ sacct -j 12345 --format=JobID,State | grep -c FAILED
```

## Post-Processing Array Results

### Combining Results

**Merge all output files**:
```bash
#!/bin/bash
# Combine results from array job
for i in {1..100}; do
    cat results_$i.txt >> combined_results.txt
done
```

**Using Python**:
```python
import glob
import pandas as pd

# Read all result files
all_files = glob.glob("results_*.csv")
df_list = [pd.read_csv(f) for f in sorted(all_files)]

# Combine into single DataFrame
combined = pd.concat(df_list, ignore_index=True)
combined.to_csv("combined_results.csv", index=False)
```

### Checking for Missing Tasks

**Script to check completion**:
```bash
#!/bin/bash
ARRAY_ID=12345
NUM_TASKS=100

for i in $(seq 1 $NUM_TASKS); do
    if [ ! -f "results_${i}.txt" ]; then
        echo "Missing task $i"
    fi
done
```


## Troubleshooting

### Some Tasks Failed

**Find failed tasks**:
```bash
$ sacct -j 12345 --format=JobID,State | grep FAILED
```

**Rerun specific failed tasks**:
```bash
#SBATCH --array=5,12,27,33  # Only failed task IDs
```

### Out of Memory on Some Tasks

**Check memory usage**:
```bash
$ sacct -j 12345 --format=JobID,MaxRSS,ReqMem,State
```

**Solutions**:

1. Increase memory for all tasks (wastes resources)
2. Identify high-memory tasks and run separately
3. Modify code to use less memory

### Tasks Taking Too Long

**Check task times**:
```bash
$ sacct -j 12345 --format=JobID,Elapsed,State | sort -k2 -h
```

**Solutions**:

- Increase time limit if tasks timeout
- Investigate slow tasks
- Consider splitting into multiple arrays by estimated runtime

### Too Many Array Tasks

Most HPC systems limit array sizes (e.g., 1000-10000 tasks).

**If you need more**:

**Option 1**: Use multiple array submissions
```bash
$ sbatch --array=1-1000 script.sh
$ sbatch --array=1001-2000 script.sh
$ sbatch --array=2001-3000 script.sh
```

**Option 2**: Process multiple items per task
```bash
#!/bin/bash
#SBATCH --array=1-100

# Each task processes 100 files
START=$(((SLURM_ARRAY_TASK_ID - 1) * 100 + 1))
END=$((SLURM_ARRAY_TASK_ID * 100))

for i in $(seq $START $END); do
    python process.py file_$i.txt
done
```

## Advanced Array Patterns

### Nested Arrays

Process a matrix of conditions:

```bash
#!/bin/bash
#SBATCH --array=1-100  # 10x10 matrix

# Define 10 values for each parameter
PARAM1=($(seq 0.1 0.1 1.0))
PARAM2=($(seq 1 1 10))

# Calculate indices
IDX=$((SLURM_ARRAY_TASK_ID - 1))
I=$((IDX / 10))
J=$((IDX % 10))

# Run with specific parameters
./simulation ${PARAM1[$I]} ${PARAM2[$J]}
```

### Dynamic Task Generation

Generate task list dynamically:

```bash
#!/bin/bash
#SBATCH --array=1-$(wc -l < task_list.txt)

# Read task from list
TASK=$(sed -n "${SLURM_ARRAY_TASK_ID}p" task_list.txt)

# Execute task
eval $TASK
```

## Example: Complete Data Processing Pipeline

```bash
#!/bin/bash
#SBATCH --job-name=data_pipeline
#SBATCH --output=logs/pipeline_%A_%a.out
#SBATCH --error=logs/pipeline_%A_%a.err
#SBATCH --array=1-100%20
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --time=04:00:00
#SBATCH --mail-type=ARRAY_TASKS
#SBATCH --mail-user=you@nmt.edu

# Exit on error
set -e

# Create output directories
mkdir -p results/$SLURM_ARRAY_TASK_ID

# Load modules
module purge
module load python/3.11

# Define input
INPUT_FILE=$(printf "data/input_%03d.txt" $SLURM_ARRAY_TASK_ID)
OUTPUT_DIR="results/$SLURM_ARRAY_TASK_ID"

# Check input exists
if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: $INPUT_FILE not found"
    exit 1
fi

# Process
echo "Processing $INPUT_FILE"
python preprocess.py --input $INPUT_FILE --output $OUTPUT_DIR/preprocessed.dat
python analyze.py --input $OUTPUT_DIR/preprocessed.dat --output $OUTPUT_DIR/results.txt
python visualize.py --input $OUTPUT_DIR/results.txt --output $OUTPUT_DIR/plot.png

echo "Task $SLURM_ARRAY_TASK_ID completed successfully"
```

## Questions?

For questions about job arrays, contact <hpc@nmthpc.atlassian.net>.
