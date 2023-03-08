#### import the simple module from the paraview
from paraview.simple import *
# Import the os module
import os
import math
import sys

case_path = sys.argv[1]
os.chdir(case_path)
time_step = sys.argv[2]

# general parameters for image saved
# DPI is resolution, width and height are the image sizes
DPI = 600
width = math.floor(4.5 * DPI)
height = math.floor(4.5 * DPI)

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(registrationName='case.foam', FileName='{}/case.foam'.format(os.getcwd()))
casefoam.SkipZeroTime = 0

# get animation scene
animationScene1 = GetAnimationScene()
# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get list of time steps
time_steps = animationScene1.TimeKeeper.TimestepValues
### If there are no time directories skip post-processing
if len(time_steps)==1:
    quit() 
# Go to certain time step
animationScene1.AnimationTime = int(time_step)

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=casefoam)

UpdatePipeline(time=0.0, proxy=threshold1)
# Properties modified on threshold1
threshold1.Scalars = ['POINTS', 'alpha.water']
# Properties modified on threshold1
threshold1.ThresholdRange = [0.51, 1.01]

# create a new 'Integrate Variables'
integrateVariables1 = IntegrateVariables(registrationName='IntegrateVariables1', Input=threshold1)

UpdatePipeline(time=0.0, proxy=integrateVariables1)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
integrateVariables1Display = Show(integrateVariables1, spreadSheetView1, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# Properties modified on spreadSheetView1
spreadSheetView1.FieldAssociation = 'Cell Data'
# Create last time step directory in post-process to save screenshots in
os.makedirs('{}/post-processing/'.format(os.getcwd()), exist_ok=True)
dir_to_safe = '{}/post-processing/'.format(os.getcwd())
# export view
ExportView('{}averages-{}.csv'.format(dir_to_safe, time_step), view=spreadSheetView1)

