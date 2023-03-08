# Post-processing scripts
This folder contains Python, Shell and Paraview scripts I used for the automatic batch post-processing of [OpenFOAM](https://www.openfoam.com/) simulations results as part of my PhD journey.

## Description
There are three types of code written and used:
1. Employing Paraview's Python API for visualization and data extractions of simulation files. (~10<sup>7</sup> number points per simulation)
2. Using Python's Matplotlib library to create nice figures with the data extracted
3. Shell scripts

### Paraview + Python + Shell
All scripts in the main folder are used for Paraview post-processing. They employ `OpenFOAMReader` from the Paraview API to read the simulation files created by [OpenFOAM-v1812](https://openfoam.org/) (can be used pretty much with any version of OpenFOAM). If you are using other input formats this reader needs to be modified accordingly.

All the code is in `*.py` files that are launched using `*.sh` scripts with the same file name.

Scripts specify required image sizes and DPI as to conform to the aimed publication page width and length.

Example: for VTK format one can use LegacyVTKReader. Sidenote: as you might guess from the name it will be depricated soon.

### Shell scripts

Are serving several purposes:
1. Launch Python code for post-processing using Paraview's API
2. Launch OpenFOAM related processes in the cluster/cloud
3. Synchronization with cluster/cloud using `rsync`

### Python Matplotlib
`matplotlib` folder contains scripts used for creation of nice figures with the specified image size.

P.S. This scripts took some time for development but saved a lot of time and nerves in turn!) Hope someone will find them useful.