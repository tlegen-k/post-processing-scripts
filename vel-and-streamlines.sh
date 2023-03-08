#!/bin/sh
# time folder
time=0.1

pvpy="/Applications/ParaView-5.9.0.app/Contents/bin/pvpython"
script_pwd="${PWD}/vel-and-streamlines.py"
fields=("alpha.water" "epsilon" "k" "nut" "p" "U")

parent_dir="$(dirname "$PWD")"

sim_folders=("${parent_dir}/umax-14.47/I-6/" "${parent_dir}/umax-17.10/I-6/" "${parent_dir}/umax-19.74/I-6/" "${parent_dir}/umax-22.37/I-6/" "${parent_dir}/umax-39.47/I-6/")

for folder in ${!sim_folders[@]}; do
    $pvpy $script_pwd ${sim_folders[$folder]} $time &
done

wait
echo "Post-processing is complete"