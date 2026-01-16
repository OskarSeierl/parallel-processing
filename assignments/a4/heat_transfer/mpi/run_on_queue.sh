#!/bin/bash

#PBS -N run_jacobi_oskar
#PBS -o run_jacobi.out
#PBS -e run_jacobi.err
#PBS -l walltime=00:30:00
#PBS -l nodes=8:ppn=8

## Start 
## Run make in the src folder (modify properly)
module load openmpi/1.8.3
cd /home/parallel/parlab48/assignments-upload/assignments/a4/heat_transfer/mpi/

sizes='2048 4096 6144'

threads=('1' '2' '4' '8' '16' '32' '64')

nodes=('1' '1' '2' '2' '4' '4' '8')
ppn=('1' '2' '2' '4' '4' '8' '8')

for size in $sizes
do
    for i in "${!threads[@]}"
    do
        echo "size: $size, threads: ${threads[i]}"
        mpirun --mca btl tcp,self -np "${threads[i]}" ./mpi_jacobi $size $size "${nodes[i]}" "${ppn[i]}"
    done
done