#!/bin/bash

# time folder
time=0.1

pvpy="/Applications/ParaView-5.9.0.app/Contents/bin/pvpython"
script_pwd="${PWD}/make-figures-x2.py"
sim_folders=("${PWD}/umax-15.79/I-6/" "${PWD}/umax-18.42/I-6/" "${PWD}/umax-21.05/I-6/" "${PWD}/umax-15.79/I-6-simple-BC/" "${PWD}/umax-18.42/I-6-simple-BC/" "${PWD}/umax-21.05/I-6-simple-BC/")
fields=("alpha.water" "epsilon" "k" "nut" "p" "U")

for folder in ${!sim_folders[@]}; do
    for i in ${!fields[@]}; do
        $pvpy $script_pwd ${sim_folders[$folder]} $time ${fields[$i]} &
    done
    wait
done

sim_folders_2=("${PWD}/umax-14.47/I-6/" "${PWD}/umax-17.10/I-6/" "${PWD}/umax-19.74/I-6/" "${PWD}/umax-22.37/I-6/" "${PWD}/umax-25/I-6/" "${PWD}/umax-39.47/I-6/")
fields=("alpha.water" "epsilon" "k" "nut" "p" "U")

for folder in ${!sim_folders_2[@]}; do
    for i in ${!fields[@]}; do
        $pvpy $script_pwd ${sim_folders_2[$folder]} $time ${fields[$i]} &
    done
    wait
done

echo "Post-processing is complete"