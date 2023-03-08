#!/bin/bash

# Script to synchronize simulation files with the MGHPCC
# How to use:
# 1. Go to the local folder with the simulation files
# 2. Correct rel_path in the script
# 3. Run script
# Profit!

# working from current folder
# assume the folders on MGHPCC are in the same relative path to 'solver-tests'
cur_folder="$PWD/"
echo $cur_folder

# modify this path only to get correct behaviour
rel_path="simulations/"

source_folder="user@cluster.org:/project/solver-tests/$rel_path"
echo $source_folder

rsync -av --exclude={'processor*','run.log','myjob.*','*.py','*.sh'} -e ssh "$source_folder" "$cur_folder"