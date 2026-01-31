# R

This guide covers using R for statistical computing and data analysis on NMTHPC.

## Loading R

```bash
$ module avail r
$ module load r/4.3.0
```

**Verify installation**:
```bash
$ R --version
$ which R
```

## Running R

### Interactive R Session

**On compute node** (recommended):
```bash
$ srun --mem=16G --time=02:00:00 --pty bash
$ module load r/4.3.0
$ R
```

**In R session**:
```r
> print("Hello from NMTHPC")
> q()  # Quit R
```

### R Scripts

**Create script** (`analysis.R`):
```r
# Load libraries
library(ggplot2)
library(dplyr)

# Read data
data <- read.csv("data.csv")

# Analysis
summary_stats <- data %>%
  group_by(category) %>%
  summarize(mean_value = mean(value))

# Plot
plot <- ggplot(data, aes(x=category, y=value)) +
  geom_boxplot()

# Save
ggsave("plot.png", plot, width=8, height=6)
write.csv(summary_stats, "results.csv")
```

**Run script non-interactively**:
```bash
$ R CMD BATCH analysis.R
$ Rscript analysis.R
```

## Batch R Jobs

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --job-name=r_analysis
#SBATCH --output=r_job_%j.out
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --time=04:00:00

module load r/4.3.0

Rscript analysis.R
```

## Installing R Packages

### Installing to User Library

**In R**:
```r
# Install packages
install.packages("ggplot2", repos="https://cloud.r-project.org")
install.packages(c("dplyr", "tidyr", "readr"))
```

Packages install to `~/R/x86_64-pc-linux-gnu-library/`

### Installing from GitHub

```r
# Install devtools first
install.packages("devtools")

# Install from GitHub
devtools::install_github("username/package")
```

### Bioconductor Packages

```r
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("DESeq2")
```

## Parallel R

### Using Multiple Cores

**parallel package**:
```r
library(parallel)

# Detect cores
num_cores <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "1"))

# Parallel apply
results <- mclapply(1:100, function(x) {
  # Your computation
  x^2
}, mc.cores=num_cores)
```

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --cpus-per-task=16
#SBATCH --mem=64G

module load r/4.3.0
Rscript parallel_script.R
```

### foreach and doParallel

```r
library(foreach)
library(doParallel)

num_cores <- as.integer(Sys.getenv("SLURM_CPUS_PER_TASK", "1"))
registerDoParallel(cores=num_cores)

results <- foreach(i=1:100, .combine='c') %dopar% {
  # Your computation
  i^2
}

stopImplicitCluster()
```

## Common R Workflows

### Data Analysis

```r
library(dplyr)
library(ggplot2)

# Load data
data <- read.csv("dataset.csv")

# Clean and transform
clean_data <- data %>%
  filter(!is.na(value)) %>%
  mutate(log_value = log(value)) %>%
  group_by(category) %>%
  summarize(
    mean_val = mean(value),
    sd_val = sd(value)
  )

# Visualize
ggplot(clean_data, aes(x=category, y=mean_val)) +
  geom_bar(stat="identity") +
  geom_errorbar(aes(ymin=mean_val-sd_val, ymax=mean_val+sd_val))

ggsave("results.png", width=10, height=6, dpi=300)
```

### Statistical Modeling

```r
# Linear regression
model <- lm(y ~ x1 + x2 + x3, data=mydata)
summary(model)

# Save model
saveRDS(model, "model.rds")

# Later: load model
loaded_model <- readRDS("model.rds")
```

## RStudio Server

Check with HPC support about RStudio Server availability for browser-based R development.

## Best Practices

1. **Save workspace**: `save.image("workspace.RData")`
2. **Load workspace**: `load("workspace.RData")`
3. **Set random seed**: `set.seed(123)` for reproducibility
4. **Use renv** for package management: `install.packages("renv")`


