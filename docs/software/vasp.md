# VASP

This guide covers using VASP (Vienna Ab initio Simulation Package) for density functional theory calculations on NMTHPC.

## VASP License

```{warning}
VASP is commercial software requiring a valid license. You must provide proof of license before accessing VASP on NMTHPC.
```

Contact <hpc@nmthpc.atlassian.net> with your VASP license information.

## Loading VASP

```bash
$ module avail vasp
$ module load vasp/6.4.3
```

```{note}
Loading the VASP module provides access to the VASP executables. If the executables are not available after loading the module, contact NMTHPC support.
```

## Running VASP

### Basic VASP Calculation

**Required input files**:
- `INCAR`: Calculation parameters
- `POSCAR`: Atomic positions
- `POTCAR`: Pseudopotentials
- `KPOINTS`: k-point mesh

**Example SLURM script**:
```bash
#!/bin/bash
#SBATCH --job-name=vasp_calc
#SBATCH --output=vasp_%j.out
#SBATCH --ntasks=16
#SBATCH --mem-per-cpu=4G
#SBATCH --time=24:00:00

module load vasp/6.4.3

mpirun vasp_std
```

### VASP Variants

**Standard version** (vasp_std):
```bash
mpirun vasp_std
```

**Gamma-point only** (vasp_gam):
```bash
mpirun vasp_gam
```

**Non-collinear** (vasp_ncl):
```bash
mpirun vasp_ncl
```

## GPU-Accelerated VASP

**For GPU nodes**:
```bash
#!/bin/bash
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --ntasks=4
#SBATCH --mem=64G
#SBATCH --time=48:00:00

module load vasp/6.4.3-gpu

mpirun vasp_gpu
```

## Example Calculations

### Structural Optimization

**INCAR**:
```
ISTART = 0
ICHARG = 2
ENCUT = 500
ISMEAR = 0
SIGMA = 0.05
IBRION = 2
NSW = 100
ISIF = 3
EDIFFG = -0.01
```

### Band Structure

**Step 1: Self-consistent calculation**:
```
ISTART = 0
ICHARG = 2
ENCUT = 500
```

**Step 2: Band structure** (INCAR):
```
ISTART = 1
ICHARG = 11
ENCUT = 500
ICHARG = 11
```

## Best Practices

1. **Test convergence**: k-points and ENCUT
2. **Checkpointing**: VASP writes WAVECAR and CHGCAR
3. **Monitor output**: Check OSZICAR during run
4. **Resource requests**: Match tasks to system
5. **Time limits**: DFT calculations can be long

## Post-Processing

**Extract energy**:
```bash
$ grep "free energy" OUTCAR | tail -1
```

**Parse OSZICAR**:
```bash
$ tail OSZICAR
```

## Questions?

Contact <hpc@nmthpc.atlassian.net> for VASP support.
