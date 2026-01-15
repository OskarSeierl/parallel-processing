#!/bin/bash

#PBS -N run_kmeans_oskar
#PBS -o run_kmeans.out
#PBS -e run_kmeans.err
#PBS -l walltime=00:30:00
#PBS -l nodes=8:ppn=8

## Start 
## Run make in the src folder (modify properly)
module load openmpi/1.8.3
cd /home/parallel/parlab48/assignments-upload/assignments/a4/kmeans

mpis='1 2 4 8 16 32 64'

for p in $mpis; do
  echo "Running with ${p} MPI processes" >> results/mpi_${p}.out
  mpirun -np $p --mca btl self,tcp ./kmeans_mpi -s 256 -n 16 -c 32 -l 10 >> results/mpi_${p}.out
done