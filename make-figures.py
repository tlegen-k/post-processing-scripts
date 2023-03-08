#### import the simple module from the paraview
from paraview.simple import *
# Import the os module
import os
import math
import sys

case_path = sys.argv[1]
os.chdir(case_path)
time_step = sys.argv[2]
field = sys.argv[3]

# general parameters for image saved
# DPI is resolution, width and height are the image sizes
DPI = 600
width = math.floor(4.5 * DPI)
height = math.floor(4.5 * DPI)

file_last_time_steps = open("../last-time-steps.txt", "a")

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(registrationName='case.foam', FileName='{}/case.foam'.format(os.getcwd()))

casefoam.SkipZeroTime = 0
casefoam.MeshRegions = ['internalMesh']
# specifying this list manually
# TODO: automate this to get all the fields in the simulation file
casefoam.CellArrays = ["alpha.water","epsilon","k","nut","p","p_rgh","U"]

# get animation scene
animationScene1 = GetAnimationScene()
# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get list of time steps
time_steps = animationScene1.TimeKeeper.TimestepValues
### If there are no time directories skip post-processing
if len(time_steps)==1:
    quit() 
# Print the current working directory
# print("Available time steps:{}".format(time_steps))
last_time_step = time_steps[-1]
# Add last time step to file
file_last_time_steps.write(str(last_time_step)+"\n")
# Go to certain time step
animationScene1.AnimationTime = last_time_step

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# show data in view
casefoamDisplay = Show(casefoam, renderView1, 'UnstructuredGridRepresentation')

fieldLUT = GetColorTransferFunction(field)
fieldPWF = GetOpacityTransferFunction(field)
renderView1.ResetCamera()
renderView1.InteractionMode = '2D'
casefoamDisplay.DataAxesGrid.GridAxesVisibility = 1

# Properties modified on casefoamDisplay.DataAxesGrid
casefoamDisplay.DataAxesGrid.XTitle = 'X'
casefoamDisplay.DataAxesGrid.YTitle = 'Y'
casefoamDisplay.DataAxesGrid.ZTitle = 'Z'
casefoamDisplay.DataAxesGrid.XTitleFontFamily = 'Arial'
# Properties modified on casefoamDisplay.DataAxesGrid
size = 48
casefoamDisplay.DataAxesGrid.XLabelFontFamily = 'Arial'
casefoamDisplay.DataAxesGrid.YLabelFontFamily = 'Arial'
casefoamDisplay.DataAxesGrid.ZLabelFontFamily = 'Arial'
casefoamDisplay.DataAxesGrid.XLabelFontSize = size 
casefoamDisplay.DataAxesGrid.YLabelFontSize = size 
casefoamDisplay.DataAxesGrid.ZLabelFontSize = size 

layout1 = GetLayout()
layout1.SetSize(1280, 720)
ColorBy(casefoamDisplay, ('POINTS', field)) 

color_bar_location = 'AnyLocation'
color_bar_position = [0.75, 0.3]
color_bar_length = 0.4
casefoamDisplay.RescaleTransferFunctionToDataRange(False, True)

fieldLUTColorBar = GetScalarBar(fieldLUT, renderView1)

fieldLUTColorBar.Position = color_bar_position
fieldLUTColorBar.ScalarBarLength = 0.4

fieldLUTColorBar.ScalarBarThickness = 10
fieldLUTColorBar.Title = field

if field == "U":
    fieldLUTColorBar.ComponentTitle = 'Magnitude'
else:
    fieldLUTColorBar.ComponentTitle = ''


# # # Properties modified on uLUTColorBar
fieldLUTColorBar.TitleFontFamily = 'Arial'

# # # Properties modified on uLUTColorBar
fieldLUTColorBar.LabelFontFamily = 'Arial'


# Create last time step directory in post-process to save screenshots in
os.makedirs('{}/post-processing/{}'.format(os.getcwd(),last_time_step), exist_ok=True)
time_dir_to_safe = '{}/post-processing/{}'.format(os.getcwd(),last_time_step)

# rescale color and/or opacity maps used to exactly fit the current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(False, True)

# save screenshot
SaveScreenshot('{}/{}.png'.format(time_dir_to_safe,field), renderView1, ImageResolution=[width, height])

    
fieldSnap = '{}/{}.png'.format(time_dir_to_safe,field)

cmd = "sips -s dpiHeight " + str(float(DPI)) + " -s dpiWidth " + str(float(DPI)) + " " + fieldSnap
file_last_time_steps.close()
os.system(cmd)
# os.remove("case.foam")