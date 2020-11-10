#!/bin/bash
#SBATCH --job-name="posi-bal"
#SBATCH --partition=compute
#SBATCH --nodes=17
#SBATCH --ntasks-per-node=24
#SBATCH -t 01:00:00
#SBATCH -A TG-DMS190038

python -m scoop posterior-run-balanced.py 