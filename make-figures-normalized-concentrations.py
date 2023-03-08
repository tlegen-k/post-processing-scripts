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
max_in_conc = sys.argv[4]

# general parameters for image saved
# DPI is resolution, width and height are the image sizes
DPI = 600
width = math.floor(3 * DPI)
height = math.floor(3 * DPI)

file_last_time_steps = open("../last-time-steps.txt", "a")

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(registrationName='case.foam', FileName='{}/case.foam'.format(os.getcwd()))

casefoam.SkipZeroTime = 0
casefoam.MeshRegions = ['internalMesh']
# specifying this list manually
# TODO: automate this to get all the fields in the simulation file
casefoam.CellArrays = ["alpha.water","epsilon","k","nut","p","p_rgh","U","H2O2","HNO2","N2O4","NO","NO2","OH"]

# get animation scene
animationScene1 = GetAnimationScene()
# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get list of time steps
time_steps = animationScene1.TimeKeeper.TimestepValues
### If there are no time directories skip post-processing
if len(time_steps)==1:
    quit() 

last_time_step = time_steps[-1]
# Add last time step to file
file_last_time_steps.write(str(last_time_step)+"\n")
# Go to certain time step
animationScene1.AnimationTime = last_time_step

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# show data in view
casefoamDisplay = Show(casefoam, renderView1, 'UnstructuredGridRepresentation')

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=casefoam)
calculator1.Function = '{}/{}'.format(field, max_in_conc)

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')
# hide data in view
Hide(casefoam, renderView1)
calculator1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')
# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
resultLUT.ApplyPreset('Linear Green (Gr4L)', True)

renderView1.ResetCamera()
renderView1.InteractionMode = '2D'

layout1 = GetLayout()
layout1.SetSize(1280, 720)
# ColorBy(casefoamDisplay, ('POINTS', field)) 

color_bar_location = 'AnyLocation'
color_bar_position = [0.7, 0.3]
color_bar_length = 0.4
color_bar_thickness = 30
size = 16
font = 'Arial'

resultLUTColorBar.Position = color_bar_position
resultLUTColorBar.ScalarBarLength = 0.4

resultLUTColorBar.ScalarBarThickness = 20
resultLUTColorBar.Title = field
resultLUTColorBar.TitleFontFamily = font
resultLUTColorBar.LabelFontFamily = font
resultLUTColorBar.TitleFontSize = size
resultLUTColorBar.LabelFontSize = size

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.0, 0.0]
# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]
# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')
contour1 = Contour(registrationName='Contour1', Input=slice1)

contour1.ContourBy = ['POINTS', field]
contour1.PointMergeMethod = 'Uniform Binning'
# show data in view
contour1Display = Show(contour1, renderView1, 'GeometryRepresentation')
# turn off scalar coloring
ColorBy(contour1Display, None)


# isocontours range for H2O2 in 1e-3-continued folder for t=1.001 sec
contour1.Isosurfaces = [0.0006184426269531252, 0.0028705563914957787, 0.0133239424930226, 0.06184426269531253, 0.2870556391495779, 1.3323942493022594, 6.184426269531253, 28.705563914957757, 133.23942493022594, 618.4426269531252]

# isocontours range for HNO2 in 1e-3-continued folder for t=1.001 sec
# contour1.Isosurfaces = [0.004158388183593749, 0.01930152815879607, 0.08958975757353047, 0.415838818359375, 1.9301528158796069, 8.958975757353041, 41.5838818359375, 193.0152815879605, 895.8975757353041, 4158.388183593749]

# Properties modified on contour1Display
contour1Display.LineWidth = 2.0
# change solid color
contour1Display.AmbientColor = [1.0, 1.0, 1.0]
contour1Display.DiffuseColor = [1.0, 1.0, 1.0]
# update the view to ensure updated data information
renderView1.Update()
# Create last time step directory in post-process to save screenshots in
os.makedirs('{}/post-processing/{}'.format(os.getcwd(),last_time_step), exist_ok=True)
time_dir_to_safe = '{}/post-processing/{}'.format(os.getcwd(),last_time_step)

# rescale color and/or opacity maps used to exactly fit the current data range
casefoamDisplay.RescaleTransferFunctionToDataRange(False, True)

fieldSnap = '{}/{}-normalized.png'.format(time_dir_to_safe,field)
# save screenshot
SaveScreenshot(fieldSnap, renderView1, ImageResolution=[width, height])

    

cmd = "sips -s dpiHeight " + str(float(DPI)) + " -s dpiWidth " + str(float(DPI)) + " " + fieldSnap
file_last_time_steps.close()
os.system(cmd)
# os.remove("case.foam")