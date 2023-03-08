#!/bin/bash

pvpy="/Applications/ParaView-5.9.0.app/Contents/bin/pvpython"
script_pwd="${PWD}/averages.py"
sim_folders=("${PWD}/with/" "${PWD}/without/")

# $pvpy $script_pwd ${sim_folders[0]} $time 

# time folder
time=0.01

for folder in ${!sim_folders[@]}; do
    $pvpy $script_pwd ${sim_folders[$folder]} $time &
done
wait

time=0.1
for folder in ${!sim_folders[@]}; do
    $pvpy $script_pwd ${sim_folders[$folder]} $time &
done
wait

time=0.2
for folder in ${!sim_folders[@]}; do
    $pvpy $script_pwd ${sim_folders[$folder]} $time &
done
wait

echo "Post-processing is complete"