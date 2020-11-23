#!/bin/bash
#SBATCH --job-name="oposi-std"
#SBATCH --partition=compute
#SBATCH --nodes=32
#SBATCH --ntasks-per-node=24
#SBATCH -t 01:00:00
#SBATCH -A TG-DMS190038

python -m scoop posterior-run-stdized.py
