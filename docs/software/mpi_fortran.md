# Using MPI with Fortran

This guide covers parallel programming with MPI (Message Passing Interface) and Fortran on NMTHPC.

## MPI on NMTHPC

### Available MPI Implementations

```bash
$ module avail openmpi
$ module avail mpich
$ module avail intel-mpi
```

**Load MPI**:
```bash
$ module load gcc/11.2.0
$ module load openmpi/4.1.4
```

## Compiling MPI Fortran Code

### MPI Fortran Compiler

**Compile Fortran + MPI**:
```bash
$ module load gcc/11.2.0
$ module load openmpi/4.1.4
$ mpifort -o my_program my_program.f90
```

**With optimization**:
```bash
$ mpifort -O3 -o my_program my_program.f90
```

## Basic MPI Fortran Program

**hello_mpi.f90**:
```fortran
program hello_mpi
    use mpi
    implicit none

    integer :: ierr, rank, size

    call MPI_Init(ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)

    print *, 'Hello from rank', rank, 'of', size

    call MPI_Finalize(ierr)
end program hello_mpi
```

**Compile and run**:
```bash
$ mpifort -o hello_mpi hello_mpi.f90
$ mpirun -np 4 ./hello_mpi
```

## Running MPI Jobs

### Interactive MPI Job

```bash
$ srun --ntasks=16 --pty bash
$ module load gcc/11.2.0
$ module load openmpi/4.1.4
$ mpirun -np 16 ./my_program
```

### Batch MPI Job

**SLURM script**:
```bash
#!/bin/bash
#SBATCH --job-name=mpi_job
#SBATCH --output=mpi_%j.out
#SBATCH --ntasks=32
#SBATCH --mem-per-cpu=2G
#SBATCH --time=12:00:00

module load gcc/11.2.0
module load openmpi/4.1.4

mpirun ./my_mpi_program
```

```{note}
With SLURM, `mpirun` automatically uses the allocated tasks. No need to specify `-np`.
```

## MPI Communication Examples

### Point-to-Point Communication

```fortran
program mpi_send_recv
    use mpi
    implicit none

    integer :: ierr, rank, size
    integer :: send_data, recv_data
    integer :: status(MPI_STATUS_SIZE)

    call MPI_Init(ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)

    if (rank == 0) then
        send_data = 42
        call MPI_Send(send_data, 1, MPI_INTEGER, 1, 0, MPI_COMM_WORLD, ierr)
        print *, 'Rank 0 sent:', send_data
    else if (rank == 1) then
        call MPI_Recv(recv_data, 1, MPI_INTEGER, 0, 0, MPI_COMM_WORLD, status, ierr)
        print *, 'Rank 1 received:', recv_data
    end if

    call MPI_Finalize(ierr)
end program mpi_send_recv
```

### Collective Communication

**Broadcast**:
```fortran
integer :: data

if (rank == 0) then
    data = 100
end if

call MPI_Bcast(data, 1, MPI_INTEGER, 0, MPI_COMM_WORLD, ierr)
```

**Reduce**:
```fortran
integer :: local_sum, global_sum

local_sum = rank + 1

call MPI_Reduce(local_sum, global_sum, 1, MPI_INTEGER, &
                MPI_SUM, 0, MPI_COMM_WORLD, ierr)

if (rank == 0) then
    print *, 'Global sum:', global_sum
end if
```

## Parallel Array Operations

**Distribute array across processes**:
```fortran
program parallel_sum
    use mpi
    implicit none

    integer :: ierr, rank, size
    integer :: n, local_n, i
    real(8), allocatable :: array(:), local_array(:)
    real(8) :: local_sum, global_sum

    call MPI_Init(ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)

    n = 1000
    local_n = n / size

    allocate(local_array(local_n))

    ! Initialize local array
    do i = 1, local_n
        local_array(i) = rank * local_n + i
    end do

    ! Compute local sum
    local_sum = sum(local_array)

    ! Reduce to get global sum
    call MPI_Reduce(local_sum, global_sum, 1, MPI_DOUBLE_PRECISION, &
                    MPI_SUM, 0, MPI_COMM_WORLD, ierr)

    if (rank == 0) then
        print *, 'Global sum:', global_sum
    end if

    deallocate(local_array)
    call MPI_Finalize(ierr)
end program parallel_sum
```

## Hybrid MPI + OpenMP

**Compile with OpenMP**:
```bash
$ mpifort -fopenmp -o hybrid hybrid.f90
```

**Hybrid code**:
```fortran
program hybrid_mpi_openmp
    use mpi
    use omp_lib
    implicit none

    integer :: ierr, rank, size, thread_id

    call MPI_Init(ierr)
    call MPI_Comm_rank(MPI_COMM_WORLD, rank, ierr)
    call MPI_Comm_size(MPI_COMM_WORLD, size, ierr)

    !$OMP PARALLEL PRIVATE(thread_id)
    thread_id = omp_get_thread_num()
    print *, 'MPI rank', rank, 'OpenMP thread', thread_id
    !$OMP END PARALLEL

    call MPI_Finalize(ierr)
end program hybrid_mpi_openmp
```

**SLURM script for hybrid**:
```bash
#!/bin/bash
#SBATCH --ntasks=4              # MPI processes
#SBATCH --cpus-per-task=8       # OpenMP threads per process
#SBATCH --mem-per-cpu=2G

module load gcc/11.2.0
module load openmpi/4.1.4

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

mpirun ./hybrid
```

## Best Practices

1. **Test with small tasks first**: Debug with 2-4 processes
2. **Check scaling**: Measure speedup vs. number of processes
3. **Load balancing**: Ensure work is distributed evenly
4. **Minimize communication**: Communication is expensive
5. **Use collective operations**: More efficient than point-to-point

## Performance Tuning

**Measure execution time**:
```fortran
real(8) :: start_time, end_time

start_time = MPI_Wtime()

! Your computation

end_time = MPI_Wtime()

if (rank == 0) then
    print *, 'Time:', end_time - start_time, 'seconds'
end if
```

## Questions?

Contact <hpc-support@nmt.edu> for MPI and Fortran support.
