#!/bin/bash

## Give the Job a descriptive name
#PBS -N run_kmeans_oskar

## Output and error files
#PBS -o run_kmeans.out
#PBS -e run_kmeans.err

##How long should the job run for?
#PBS -l walltime=00:30:00

## Start 
## Run make in the src folder (modify properly)

cd /home/parallel/parlab48/assignments-upload/assignments/a4/kmeans

sizes='256'
coordinates='16'
centers='32'
loop_threashold='10'
mpis='1 2 4 8 16 32 64'

progs=(
	kmeans
)

for size in $sizes; do
	for coord in $coordinates; do
		for center in $centers; do
			filename=Execution_logs/Sz-${size}_Coo-${coord}_Cl-${center}.csv 
			echo "Implementation,blockSize,av_loop_t,min_loop_t,max_loop_t,t_cpu_avg,t_gpu_avg,t_transfers_avg" >> $filename
			for prog in "${progs[@]}"; do
				for bs in $mpis; do
				  ./${prog} -s $size -n $coord -c $center -l $loop_threashold
				done
			done
		done
	done
done
