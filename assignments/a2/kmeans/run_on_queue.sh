#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans

## Output and error files
#PBS -o run_kmeans.out
#PBS -e run_kmeans.err

## How many machines should we get? 
#PBS -l nodes=1:ppn=8

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

cd /home/parallel/parlab48/assignments-upload/assignments/a2/kmeans
export OMP_NUM_THREADS=8

# Change according to exercise description here:
# also changed called programm, e.g. ./kmeans_omp_naive ...
#./kmeans_seq -s <SIZE> -n <COORDS> -c <CLUSTERS> -l <LOOPS>
./kmeans_seq -s 256 -n 16 -c 32 -l 10
