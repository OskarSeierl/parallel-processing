#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_fw

## Output and error files
#PBS -o out/run_fw.out
#PBS -e out/run_fw.err

## How many machines should we get? 
#PBS -q serial
#PBS -l nodes=sandman:ppn=64

##How long should the job run for?
#PBS -l walltime=00:10:00

## Start 
## Run make in the src folder (modify properly)

# Not needed, already done by setting flags in Makefile
# module load openmp

cd /home/parallel/parlab48/assignments-upload/assignments/a2/FW
export OMP_NUM_THREADS=8
# ./fw <SIZE>
./fw_sr <SIZE> <BSIZE>
# ./fw_tiled <SIZE> <BSIZE>
