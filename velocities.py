# trace generated using paraview version 5.9.0
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
width = math.floor(3 * DPI)
height = math.floor(3 * DPI)

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

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
    print("No time steps to write")

last_time_step = time_steps[-1]
# Go to last time step
animationScene1.AnimationTime = last_time_step

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# show data in view
casefoamDisplay = Show(casefoam, renderView1, 'UnstructuredGridRepresentation')

# #change interaction mode for render view
renderView1.InteractionMode = '2D'

# # trace defaults for the display properties.
casefoamDisplay.Representation = 'Surface'

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=casefoam)
threshold1.Scalars = ['POINTS', 'alpha.water']
threshold1.ThresholdRange = [-0.01, 0.49]

# show data in view
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(casefoam, renderView1)

# set scalar coloring
ColorBy(threshold1Display, ('POINTS', 'U', 'Magnitude'))

# create a new 'Threshold'
threshold2 = Threshold(registrationName='Threshold2', Input=casefoam)
threshold2.Scalars = ['POINTS', 'alpha.water']
threshold2.ThresholdRange = [0.51, 1.01]

# show data in view
threshold2Display = Show(threshold2, renderView1, 'UnstructuredGridRepresentation')

# set scalar coloring
ColorBy(threshold2Display, ('POINTS', 'alpha.water'))

# # create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=threshold2)
calculator1.Function = 'U'

# Properties modified on calculator1
calculator1.ResultArrayName = 'U_w'
# update the view to ensure updated data information
renderView1.Update()
# # # show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')


# # hide data in view
Hide(threshold2, renderView1)

# set scalar coloring
ColorBy(calculator1Display, ('POINTS', 'U_w', 'Magnitude'))

# set active source
SetActiveSource(threshold1)

size = 10 
font = 'Arial'
color_bar_length = 0.4
color_bar_thickness = 20

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')
# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# Rescale transfer function
uLUT.RescaleTransferFunction(0.0, 22.37)
uPWF.RescaleTransferFunction(0.0, 22.37)

# get color legend/bar for uLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)
uLUTColorBar.WindowLocation = 'AnyLocation'
uLUTColorBar.ComponentTitle = 'Magnitude'

# # Properties modified on uLUTColorBar
uLUTColorBar.Title = 'Uair'
uLUTColorBar.ScalarBarLength = color_bar_length 
uLUTColorBar.ScalarBarThickness = color_bar_thickness
# # Properties modified on uLUTColorBar
uLUTColorBar.Orientation = 'Vertical'
# uLUTColorBar.Orientation = 'Horizontal'

# Properties modified on uLUTColorBar
uLUTColorBar.TitleFontFamily = font
uLUTColorBar.TitleFontSize = size

# Properties modified on uLUTColorBar
uLUTColorBar.LabelFontFamily = font
uLUTColorBar.LabelFontSize = size
# Properties modified on uLUTColorBar
uLUTColorBar.DrawTickMarks = 1

# Properties modified on uLUTColorBar
uLUTColorBar.DrawTickLabels = 1
# uLUTColorBar.UseCustomLabels = 1
# uLUTColorBar.CustomLabels = xrange(0, 21, 4)

# Properties modified on uLUTColorBar
uLUTColorBar.Position = [0.67, 0.55]


# set active source
SetActiveSource(calculator1)

# # get color transfer function/color map for 'U_w'
u_wLUT = GetColorTransferFunction('U_w')
u_wLUT.NanColor = [1.0, 0.0, 0.0]
u_wLUT.ScalarRangeInitialized = 1.0

# # # get opacity transfer function/opacity map for 'U_w'
u_wPWF = GetOpacityTransferFunction('U_w')
u_wPWF.Points = [0.0, 0.0, 0.5, 0.0, 0.12363082272768557, 1.0, 0.5, 0.0]
u_wPWF.ScalarRangeInitialized = 1
u_wLUT.RescaleTransferFunction(0.0, 0.045)
u_wPWF.RescaleTransferFunction(0.0, 0.045)

# # hide data in view
Hide(casefoam, renderView1)

# # get color legend/bar for u_wLUT in view renderView1
u_wLUTColorBar = GetScalarBar(u_wLUT, renderView1)
u_wLUTColorBar.ComponentTitle = 'Magnitude'
u_wLUTColorBar.Title = 'Uwater'
u_wLUTColorBar.WindowLocation = 'AnyLocation'
u_wLUTColorBar.ScalarBarLength = color_bar_length 
u_wLUTColorBar.Orientation = 'Vertical'
u_wLUTColorBar.Position = [0.67, 0.09]
u_wLUTColorBar.ScalarBarThickness = color_bar_thickness

# Properties modified on u_wLUTColorBar
u_wLUTColorBar.TitleFontFamily = font
u_wLUTColorBar.TitleFontSize = size

# Properties modified on u_wLUTColorBar
u_wLUTColorBar.LabelFontFamily = font
u_wLUTColorBar.LabelFontSize = size

# Create last time step directory in post-process to save screenshots in
os.makedirs('{}/post-processing/{}'.format(os.getcwd(),last_time_step), exist_ok=True)
time_dir_to_safe = '{}/post-processing/{}'.format(os.getcwd(),last_time_step)

uSnap = '{}/velocities-{}.png'.format(time_dir_to_safe, last_time_step)

# save screenshot
SaveScreenshot(uSnap, renderView1, ImageResolution=[width, height])

cmd = "sips -s dpiHeight " + str(float(DPI)) + " -s dpiWidth " + str(float(DPI)) + " " + uSnap
os.system(cmd)
