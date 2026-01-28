# Python and Jupyter Notebooks

This guide covers using Python and Jupyter Notebooks on NMTHPC for interactive computing and data analysis.

## Python on NMTHPC

### Loading Python

**System Python modules**:
```bash
$ module avail python
$ module load python/3.11
```

**Using Anaconda** (recommended):
```bash
$ module load anaconda3
```

See [Anaconda](anaconda.md) for comprehensive environment management.

### Verifying Python

```bash
$ python --version
$ which python
```

## Running Python Scripts

### Interactive Python

**On login node** (light work only):
```bash
$ module load python/3.11
$ python
>>> print("Hello from NMTHPC")
```

**On compute node** (recommended):
```bash
$ srun --pty bash
$ module load python/3.11
$ python my_script.py
```

### Batch Python Jobs

```bash
#!/bin/bash
#SBATCH --job-name=python_job
#SBATCH --output=python_%j.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=04:00:00

module load python/3.11

python analysis.py --input data.csv --output results.txt
```

## Installing Python Packages

### Using pip

**User installation** (in home directory):
```bash
$ module load python/3.11
$ pip install --user numpy pandas matplotlib
```

**Check installed packages**:
```bash
$ pip list --user
```

### Using Conda (Recommended)

**Create environment**:
```bash
$ module load anaconda3
$ conda create -n myenv python=3.11 numpy pandas matplotlib
$ conda activate myenv
```

See [Anaconda](anaconda.md) for detailed instructions.

### Virtual Environments (venv)

**Create virtual environment**:
```bash
$ module load python/3.11
$ python -m venv ~/myproject_env
$ source ~/myproject_env/bin/activate
$ pip install numpy pandas matplotlib
```

**Use in job script**:
```bash
#!/bin/bash
#SBATCH directives...

module load python/3.11
source ~/myproject_env/bin/activate

python my_script.py
```

## Jupyter Notebooks

Jupyter Notebooks provide an interactive computing environment ideal for data exploration, visualization, and sharing results.

### Setting Up Jupyter

**Create Jupyter environment**:
```bash
$ module load anaconda3
$ conda create -n jupyter python=3.11 jupyter numpy pandas matplotlib scikit-learn
$ conda activate jupyter
```

### Running Jupyter on NMTHPC

```{warning}
Do not run Jupyter directly on login nodes. Always use compute nodes via SLURM.
```

### Method 1: Interactive Job with SSH Tunnel

**Step 1: Start interactive job**:
```bash
$ srun --ntasks=1 --cpus-per-task=4 --mem=16G --time=04:00:00 --pty bash
```

**Step 2: On compute node, load and start Jupyter**:
```bash
$ module load anaconda3
$ conda activate jupyter
$ jupyter notebook --no-browser --ip=0.0.0.0 --port=8888
```

**Note the node name and token** from output:
```
http://node05:8888/?token=abc123...
```

**Step 3: In new local terminal, create SSH tunnel**:
```bash
$ ssh -L 8888:node05:8888 username@hpc.nmt.edu
```

Replace `node05` with your actual compute node.

**Step 4: Open browser locally**:
```
http://localhost:8888
```

Paste the token when prompted.

### Method 2: Batch Job with Jupyter

**Not recommended for interactive work**, but useful for executing notebooks:

```bash
#!/bin/bash
#SBATCH --job-name=jupyter_exec
#SBATCH --output=jupyter_%j.out
#SBATCH --mem=16G
#SBATCH --time=02:00:00

module load anaconda3
conda activate jupyter

# Execute notebook non-interactively
jupyter nbconvert --to notebook --execute my_notebook.ipynb --output executed_notebook.ipynb
```

### Jupyter with GPU

**Request GPU for Jupyter session**:
```bash
$ srun --partition=gpu --gres=gpu:1 --mem=32G --time=04:00:00 --pty bash
$ module load anaconda3
$ conda activate jupyter
$ jupyter notebook --no-browser --ip=0.0.0.0 --port=8888
```

Then create SSH tunnel as above.

See [Running Jobs on GPU Nodes](../using_nmthpc/gpu_jobs.md) for more GPU information.

## Parallel Python

### NumPy/SciPy Multithreading

**Control thread count**:
```bash
#!/bin/bash
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G

module load python/3.11

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export MKL_NUM_THREADS=$SLURM_CPUS_PER_TASK

python compute_intensive.py
```

### Multiprocessing

**Python multiprocessing example**:
```python
from multiprocessing import Pool
import os

def process_data(x):
    # Your processing function
    return x * x

if __name__ == '__main__':
    # Use number of allocated CPUs
    n_workers = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))

    with Pool(n_workers) as pool:
        results = pool.map(process_data, range(100))

    print(results)
```

**Job script**:
```bash
#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=32G

module load python/3.11
python parallel_script.py
```

### Dask for Distributed Computing

**Install Dask**:
```bash
$ conda install dask distributed
```

**Dask on single node**:
```python
from dask.distributed import Client, LocalCluster
import os

# Create local cluster
n_workers = int(os.environ.get('SLURM_CPUS_PER_TASK', 1))
cluster = LocalCluster(n_workers=n_workers, threads_per_worker=1)
client = Client(cluster)

# Your Dask computations
import dask.array as da
x = da.random.random((10000, 10000), chunks=(1000, 1000))
result = x.mean().compute()

client.close()
```

## Common Python Libraries

### Scientific Computing

```bash
$ conda install numpy scipy sympy
```

**Example usage**:
```python
import numpy as np
from scipy import optimize, integrate

# Linear algebra
a = np.array([[1, 2], [3, 4]])
eigenvalues = np.linalg.eigvals(a)

# Optimization
result = optimize.minimize(lambda x: x**2, x0=1.0)
```

### Data Analysis

```bash
$ conda install pandas
```

**Example**:
```python
import pandas as pd

# Read data
df = pd.read_csv('data.csv')

# Analyze
summary = df.describe()
grouped = df.groupby('category').mean()

# Save results
grouped.to_csv('results.csv')
```

### Visualization

```bash
$ conda install matplotlib seaborn plotly
```

**Matplotlib example**:
```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(10, 6))
plt.plot(x, y)
plt.xlabel('X')
plt.ylabel('sin(X)')
plt.title('Sine Wave')
plt.savefig('sine_plot.png', dpi=300)
```

### Machine Learning

```bash
$ conda install scikit-learn
```

**Example**:
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Prepare data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Train model
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)

# Evaluate
predictions = clf.predict(X_test)
accuracy = accuracy_score(y_test, predictions)
```

See [Training AI/ML Models on GPUs](ai_ml_gpu.md) for deep learning.

## Best Practices

### Script Organization

**Modular structure**:
```
project/
├── data/
│   └── input_data.csv
├── src/
│   ├── preprocessing.py
│   ├── analysis.py
│   └── visualization.py
├── results/
├── environment.yml
└── run_analysis.sh
```

### Command-Line Arguments

**Using argparse**:
```python
import argparse

parser = argparse.ArgumentParser(description='Data analysis script')
parser.add_argument('--input', required=True, help='Input file')
parser.add_argument('--output', required=True, help='Output file')
parser.add_argument('--threads', type=int, default=1, help='Number of threads')

args = parser.parse_args()

# Use arguments
print(f"Processing {args.input}")
```

### Logging

**Set up logging**:
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis.log'),
        logging.StreamHandler()
    ]
)

logging.info("Starting analysis")
# Your code
logging.info("Analysis complete")
```

### Error Handling

```python
import sys

try:
    # Your code
    result = process_data(input_file)
except FileNotFoundError:
    logging.error(f"Input file not found: {input_file}")
    sys.exit(1)
except Exception as e:
    logging.error(f"Unexpected error: {e}")
    sys.exit(1)
```

## Example Workflows

### Data Analysis Workflow

**analysis_workflow.sh**:
```bash
#!/bin/bash
#SBATCH --job-name=data_analysis
#SBATCH --output=analysis_%j.out
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=04:00:00

module load anaconda3
conda activate analysis_env

# Run analysis pipeline
python preprocess.py --input raw_data.csv --output clean_data.csv
python analyze.py --input clean_data.csv --output results.csv
python visualize.py --input results.csv --output figures/
```

### Parameter Sweep with Job Array

**sweep.sh**:
```bash
#!/bin/bash
#SBATCH --job-name=param_sweep
#SBATCH --output=logs/sweep_%A_%a.out
#SBATCH --array=1-100
#SBATCH --mem=8G
#SBATCH --time=02:00:00

module load python/3.11

# Get parameters for this task
PARAM=$(sed -n "${SLURM_ARRAY_TASK_ID}p" parameters.txt)

python simulate.py --param $PARAM --output results_${SLURM_ARRAY_TASK_ID}.dat
```

## Troubleshooting

### Import Errors

**Check Python path**:
```bash
$ python -c "import sys; print('\n'.join(sys.path))"
```

**Verify package installation**:
```bash
$ python -c "import numpy; print(numpy.__version__)"
```

### Memory Issues

**Monitor memory usage**:
```python
import psutil
import os

process = psutil.Process(os.getpid())
print(f"Memory usage: {process.memory_info().rss / 1e9:.2f} GB")
```

**Use memory-efficient alternatives**:
- Read files in chunks: `pd.read_csv('large_file.csv', chunksize=10000)`
- Use generators instead of lists
- Delete large objects when done: `del large_array`

### Performance Issues

**Profile your code**:
```python
import cProfile
import pstats

cProfile.run('your_function()', 'profile_stats')
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)
```

**Use line_profiler** for line-by-line profiling:
```bash
$ pip install line_profiler
```

## Additional Resources

- [Anaconda](anaconda.md)
- [Training AI/ML Models on GPUs](ai_ml_gpu.md)
- [Running Batch Jobs](../using_nmthpc/batch_jobs.md)
- [Using Job Arrays](../using_nmthpc/job_arrays.md)

## Questions?

For questions about Python or Jupyter on NMTHPC, contact <hpc-support@nmt.edu>.
