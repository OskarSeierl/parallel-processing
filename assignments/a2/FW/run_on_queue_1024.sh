#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_fw_1024

## Output and error files
#PBS -o out/run_fw_1024.out
#PBS -e out/run_fw_1024.err

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start
## Run make in the src folder (modify properly)

cd /home/parallel/parlab48/assignments-upload/assignments/a2/FW

N=1024
B=64

# Run recursive implementation
for thr in 1 2 4 8 16 32 64
do
	export OMP_NUM_THREADS=$thr
	./fw_sr $N $B
done
