#!/bin/bash
#BSUB -n 1                   # Where X is in the set {1..X}
#BSUB -J latest-times        # Job Name
#BSUB -o myjob.out           # Append to output log file
#BSUB -e myjob.err           # Append to error log file
#BSUB -oo myjob.log          # Overwrite output log file 
#BSUB -eo myjob.err          # Overwrite error log file 
#BSUB -q short               # Which queue to use {short, long, parallel, GPU, interactive}
#BSUB -W 4:00                # How much time does your job need (HH:MM)

find . -mindepth 2 -maxdepth 2 -type d \( ! -name . \) -exec bash -c "cd '{}' && reconstructPar -newTimes" \;
