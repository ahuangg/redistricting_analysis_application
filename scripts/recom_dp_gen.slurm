#!/usr/bin/env bash

#SBATCH --nodes=1
#SBATCH --time=48:00:00
#SBATCH --partition=long-96core
#SBATCH --job-name=recom_testing
#SBATCH --output=recom_log_output.txt

module load gerrychain

python recom_dp_gen.py
