#!/bin/bash

#PBS -N run_jacobi_oskar
#PBS -o run_jacobi_oskar.out
#PBS -e run_jacobi.err
#PBS -l walltime=00:30:00
#PBS -l nodes=8:ppn=8

## Start 
## Run make in the src folder (modify properly)
module load openmpi/1.8.3
cd /home/parallel/parlab48/assignments-upload/assignments/a4/heat_transfer/mpi/

mpirun --mca btl tcp,self -np 64 ./mpi_jacobi 1024 1024 8 8