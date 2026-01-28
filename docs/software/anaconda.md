# Anaconda

Anaconda is a package and environment management system for Python. It's the recommended way to manage Python environments on NMTHPC.

## Why Use Anaconda?

**Benefits**:

- Create isolated environments for different projects
- Easy installation of packages and dependencies
- Manage different Python versions
- Avoid conflicts between package requirements
- Share reproducible environments with collaborators

## Loading Anaconda

```bash
$ module load anaconda3
```

**Verify installation**:
```bash
$ conda --version
$ which conda
```

## Creating Environments

### Basic Environment

**Create environment with specific Python version**:
```bash
$ conda create -n myenv python=3.11
```

**Activate the environment**:
```bash
$ conda activate myenv
```

**Deactivate when done**:
```bash
$ conda deactivate
```

### Environment with Packages

**Create environment and install packages**:
```bash
$ conda create -n data_analysis python=3.11 numpy pandas matplotlib scipy
```

**Install additional packages later**:
```bash
$ conda activate data_analysis
$ conda install scikit-learn seaborn
```

## Managing Packages

### Installing Packages

**From conda**:
```bash
$ conda install numpy scipy matplotlib
```

**From conda-forge** (larger package repository):
```bash
$ conda install -c conda-forge package_name
```

**From pip** (when package not in conda):
```bash
$ pip install package_name
```

```{tip}
Prefer `conda install` over `pip install` when possible. Conda handles dependencies better within conda environments.
```

### Listing Packages

**Packages in current environment**:
```bash
$ conda list
```

**Search for available packages**:
```bash
$ conda search package_name
```

### Updating Packages

**Update specific package**:
```bash
$ conda update numpy
```

**Update all packages**:
```bash
$ conda update --all
```

### Removing Packages

```bash
$ conda remove package_name
```

## Managing Environments

### List Environments

```bash
$ conda env list
```

or

```bash
$ conda info --envs
```

### Clone Environment

**Create copy of existing environment**:
```bash
$ conda create --name newenv --clone oldenv
```

### Remove Environment

```bash
$ conda env remove --name myenv
```

## Environment Files

### Export Environment

**Create reproducible environment file**:
```bash
$ conda activate myenv
$ conda env export > environment.yml
```

**environment.yml** contains all packages and versions.

### Create Environment from File

**On another system or for collaborators**:
```bash
$ conda env create -f environment.yml
```

### Minimal Environment File

**Manually create environment.yml**:
```yaml
name: myproject
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - numpy
  - pandas
  - matplotlib
  - scikit-learn
  - pip
  - pip:
    - some-pip-only-package
```

**Create from file**:
```bash
$ conda env create -f environment.yml
```

## Using Conda in Job Scripts

### Interactive Jobs

```bash
$ srun --pty bash
$ module load anaconda3
$ conda activate myenv
$ python my_script.py
```

### Batch Jobs

```bash
#!/bin/bash
#SBATCH --job-name=conda_job
#SBATCH --output=conda_%j.out
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --time=04:00:00

# Load anaconda
module load anaconda3

# Activate environment
source activate myenv

# Run Python script
python analysis.py
```

```{note}
Use `source activate` in batch scripts instead of `conda activate` for better compatibility.
```

## Common Environments for HPC

### Data Science Environment

```bash
$ conda create -n datascience python=3.11 \
    numpy pandas matplotlib seaborn scikit-learn \
    jupyter notebook ipython
```

### Machine Learning Environment

```bash
$ conda create -n ml python=3.11 \
    numpy pandas scikit-learn \
    pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

or for TensorFlow:
```bash
$ conda create -n tensorflow python=3.11 \
    numpy pandas matplotlib \
    tensorflow-gpu cudatoolkit=12.1
```

### Bioinformatics Environment

```bash
$ conda create -n bio python=3.11 \
    biopython pandas numpy matplotlib \
    -c bioconda -c conda-forge
```

### Scientific Computing Environment

```bash
$ conda create -n science python=3.11 \
    numpy scipy matplotlib \
    sympy numba h5py netcdf4
```

## Best Practices

### Environment Location

By default, conda creates environments in `~/.conda/envs/`.

**Check environment size**:
```bash
$ du -sh ~/.conda/envs/*
```

**Clean up cached packages**:
```bash
$ conda clean --all
```

### Naming Conventions

Use descriptive names:

- `project_name`: For specific projects
- `python311`: For general Python 3.11 environment
- `ml_gpu`: For machine learning with GPU
- `analysis_2024`: For specific analysis work

### Performance Tips

**1. Use mamba** for faster package resolution:
```bash
$ conda install -c conda-forge mamba
$ mamba install numpy pandas  # Much faster than conda
```

**2. Specify channels in environment file** to avoid conflicts:
```yaml
channels:
  - conda-forge
  - defaults
```

**3. Pin versions** for reproducibility:
```yaml
dependencies:
  - python=3.11.5
  - numpy=1.24.3
  - pandas=2.0.2
```

## Troubleshooting

### Environment Not Found

**After creating environment**:
```bash
$ conda env list  # Make sure it was created
$ conda activate myenv
```

If activation fails:
```bash
$ source activate myenv  # Try source activate
```

### Package Conflicts

**Clear conda cache**:
```bash
$ conda clean --all
```

**Create fresh environment**:
```bash
$ conda deactivate
$ conda env remove -n problematic_env
$ conda create -n problematic_env python=3.11
```

**Install packages one at a time** to identify conflicts:
```bash
$ conda install numpy
$ conda install pandas
# etc.
```

### Conda is Slow

**Use mamba** instead:
```bash
$ conda install -c conda-forge mamba
$ mamba install package_name  # Much faster
```

**Use micromamba** (lightweight alternative):
```bash
# Ask HPC support about micromamba availability
```

### Out of Disk Space

**Check environment sizes**:
```bash
$ du -sh ~/.conda/envs/*
```

**Remove unused environments**:
```bash
$ conda env remove -n unused_env
```

**Clean package cache**:
```bash
$ conda clean --all
```

**Contact HPC support** if you need more quota.

## Example Workflows

### Creating a New Project Environment

```bash
# Load anaconda
$ module load anaconda3

# Create environment
$ conda create -n myproject python=3.11

# Activate environment
$ conda activate myproject

# Install packages
$ conda install numpy pandas matplotlib scikit-learn jupyter

# Export for reproducibility
$ conda env export > environment.yml

# Test it works
$ python -c "import numpy, pandas; print('Success!')"
```

### Using Jupyter with Conda

```bash
# Create environment with Jupyter
$ conda create -n jupyter_env python=3.11 jupyter numpy pandas matplotlib

# Activate and start Jupyter
$ conda activate jupyter_env
$ jupyter notebook --no-browser --ip=0.0.0.0
```

See [Python and Jupyter Notebooks](python_jupyter.md) for detailed Jupyter instructions.

### Machine Learning Workflow

```bash
# Create ML environment
$ conda create -n pytorch_ml python=3.11
$ conda activate pytorch_ml

# Install PyTorch with GPU support
$ conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia

# Install additional packages
$ conda install pandas scikit-learn matplotlib seaborn tensorboard

# Verify GPU support
$ python -c "import torch; print(torch.cuda.is_available())"

# Export environment
$ conda env export > ml_environment.yml
```

## Conda Cheat Sheet

| Task | Command |
|------|---------|
| Load Anaconda | `module load anaconda3` |
| Create environment | `conda create -n myenv python=3.11` |
| Activate environment | `conda activate myenv` |
| Deactivate | `conda deactivate` |
| Install package | `conda install package` |
| List environments | `conda env list` |
| List packages | `conda list` |
| Export environment | `conda env export > env.yml` |
| Create from file | `conda env create -f env.yml` |
| Remove environment | `conda env remove -n myenv` |
| Clean cache | `conda clean --all` |

## Additional Resources

- [Python and Jupyter Notebooks](python_jupyter.md)
- [Training AI/ML Models on GPUs](ai_ml_gpu.md)
- [Official Conda Documentation](https://docs.conda.io/)
- [Conda Cheat Sheet PDF](https://docs.conda.io/projects/conda/en/latest/user-guide/cheatsheet.html)

## Questions?

For questions about Anaconda on NMTHPC, contact <hpc-support@nmt.edu>.
