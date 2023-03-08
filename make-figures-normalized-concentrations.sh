#!/bin/bash
time=4

pvpy="/Applications/ParaView-5.9.0.app/Contents/bin/pvpython"
script_pwd="${PWD}/make-figures-normalized-concentrations.py"
sim_folders=("${PWD}/without/" "${PWD}/1e-3-continued/" "${PWD}/1e-4-continued/" "${PWD}/1e-5-continued/")
fields=("H2O2" "HNO2" "N2O4" "NO" "NO2" "OH")

# scaling concentrations by inlet values
inlet_conc=("36.42" "182" "1" "1820" "11.4" "296")

for folder in ${!sim_folders[@]}; do
    for i in ${!fields[@]}; do
        $pvpy $script_pwd ${sim_folders[$folder]} $time ${fields[$i]} ${inlet_conc[$i]} &
    done
    wait
done
wait

echo "Post-processing is complete"