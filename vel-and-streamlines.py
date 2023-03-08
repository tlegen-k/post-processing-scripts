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

# Print the current working directory
print("Current working directory: {0}".format(os.getcwd()))

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
casefoam = OpenFOAMReader(registrationName='case.foam', FileName='{}/case.foam'.format(os.getcwd()))

casefoam.SkipZeroTime = 0
casefoam.MeshRegions = ['internalMesh']
# specifying this list manually
# TODO: automate this to get all the fields in the simulation file
casefoam.CellArrays = ["alpha.water","epsilon","k","nut","p","p_rgh","U"]

# create a new 'Threshold'
threshold1 = Threshold(registrationName='Threshold1', Input=casefoam)

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
threshold1Display = Show(threshold1, renderView1, 'UnstructuredGridRepresentation')
# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
# hide data in view
Hide(casefoam, renderView1)

# show color bar/color legend
threshold1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on threshold1
threshold1.Scalars = ['POINTS', 'alpha.water']

# get animation scene
animationScene1 = GetAnimationScene()

# animationScene1.GoToLast()
# get list of time steps
time_steps = animationScene1.TimeKeeper.TimestepValues
last_time_step = time_steps[-1]
animationScene1.AnimationTime = last_time_step

# Properties modified on threshold1
threshold1.ThresholdRange = [-0.01, 0.49]

# set scalar coloring
ColorBy(threshold1Display, ('POINTS', 'U', 'Magnitude'))

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')

# get opacity transfer function/opacity map for 'U'
uPWF = GetOpacityTransferFunction('U')

# set active source
SetActiveSource(casefoam)

# create a new 'Threshold'
threshold2 = Threshold(registrationName='Threshold2', Input=casefoam)

# show data in view
threshold2Display = Show(threshold2, renderView1, 'UnstructuredGridRepresentation')

# hide data in view
Hide(casefoam, renderView1)

# show color bar/color legend
threshold2Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(threshold1)

# set active source
SetActiveSource(threshold2)

# Properties modified on threshold2
threshold2.Scalars = ['POINTS', 'alpha.water']

# Properties modified on threshold2
threshold2.ThresholdRange = [0.51, 1.01]

# set scalar coloring
ColorBy(threshold2Display, ('POINTS', 'U', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
threshold2Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
threshold2Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(threshold1)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=threshold1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.007499999832361931, 0.009399999747984111, -0.007499999832361937]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# hide data in view
Hide(threshold1, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on slice1.SliceType
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.0, 0.0, 0.0]

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Magnitude'))

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(threshold2)

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# create a new 'Slice'
slice2 = Slice(registrationName='Slice2', Input=threshold2)
slice2.SliceType = 'Plane'
slice2.HyperTreeGridSlicer = 'Plane'
slice2.SliceOffsetValues = [0.0]

# hide data in view
Hide(threshold2, renderView1)

# Properties modified on slice2.SliceType
slice2.SliceType.Normal = [0.0, 0.0, 1.0]
# Properties modified on slice2.SliceType
slice2.SliceType.Origin = [0.0, 0.0, 0.0]

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=slice2)
calculator1.Function = ''

# show data in view
calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')
calculator1Display.Representation = 'Surface'
# hide data in view
Hide(slice2, renderView1)
renderView1.ResetCamera()
renderView1.InteractionMode = '2D'

layout1 = GetLayout()
layout1.SetSize(1280, 720)
# Properties modified on calculator1
calculator1.Function = 'U'
calculator1.AttributeType = 'Point Data'

# set scalar coloring
ColorBy(calculator1Display, ('POINTS', 'Result', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True, False)
# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)


# Properties modified on calculator1
calculator1.Function = 'U_X*iHat+U_Y*jHat'
# Properties modified on calculator1
calculator1.ResultArrayName = 'U_water'

# set scalar coloring
ColorBy(calculator1Display, ('POINTS', 'U_water', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
calculator1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# statements to remove extra color bar created
# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')
# get color legend/bar for resultLUT in view renderView1
resultLUTColorBar = GetScalarBar(resultLUT, renderView1)
# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(resultLUTColorBar, renderView1)

# get color transfer function/color map for 'U_water'
u_waterLUT = GetColorTransferFunction('U_water')
u_waterPWF = GetOpacityTransferFunction('U_water')

# Rescale transfer function
u_waterLUT.RescaleTransferFunction(0.0, 0.045)
u_waterPWF.RescaleTransferFunction(0.0, 0.045)

# set active source
SetActiveSource(slice1)


# create a new 'Calculator'
calculator2 = Calculator(registrationName='Calculator2', Input=slice1)
calculator2.Function = ''

# show data in view
calculator2Display = Show(calculator2, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
calculator2Display.Representation = 'Surface'

# hide data in view
Hide(slice1, renderView1)

# Properties modified on calculator2
calculator2.Function = 'U_X*iHat+U_Y*jHat'
# Properties modified on calculator2
calculator2.ResultArrayName = 'U_air'
# set scalar coloring
ColorBy(calculator2Display, ('POINTS', 'U_air', 'Magnitude'))

# get color transfer function/color map for 'U_air'
u_airLUT = GetColorTransferFunction('U_air')
u_airPWF = GetOpacityTransferFunction('U_air')

# Defining parameters for the figure
size = 16 
font = 'Arial'
color_bar_length = 0.4
color_bar_thickness = 30

# get color legend/bar for u_waterLUT in view renderView1
u_waterLUTColorBar = GetScalarBar(u_waterLUT, renderView1)
# change scalar bar placement
u_waterLUTColorBar.WindowLocation = 'AnyLocation'
u_waterLUTColorBar.ComponentTitle = 'Magnitude'
u_waterLUTColorBar.Title = 'Uwater'
u_waterLUTColorBar.WindowLocation = 'AnyLocation'
u_waterLUTColorBar.ScalarBarLength = color_bar_length 
u_waterLUTColorBar.Orientation = 'Vertical'
u_waterLUTColorBar.Position = [0.67, 0.09]
u_waterLUTColorBar.ScalarBarThickness = color_bar_thickness

# Properties modified on u_waterLUTColorBar
u_waterLUTColorBar.TitleFontFamily = font
u_waterLUTColorBar.TitleFontSize = size

# Properties modified on u_waterLUTColorBar
u_waterLUTColorBar.LabelFontFamily = font
u_waterLUTColorBar.LabelFontSize = size

# create a new 'Evenly Spaced Streamlines 2D'
evenlySpacedStreamlines2D1 = EvenlySpacedStreamlines2D(registrationName='EvenlySpacedStreamlines2D1', Input=calculator2)
evenlySpacedStreamlines2D1.Vectors = ['POINTS', 'U_air']
evenlySpacedStreamlines2D1.StartPosition = [0.007499999832361937, 0.009399999747984111, 0.0]

# show data in view
evenlySpacedStreamlines2D1Display = Show(evenlySpacedStreamlines2D1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
evenlySpacedStreamlines2D1Display.Representation = 'Surface'

# hide data in view
Hide(calculator2, renderView1)
# show color bar/color legend
evenlySpacedStreamlines2D1Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on evenlySpacedStreamlines2D1Display
evenlySpacedStreamlines2D1Display.LineWidth = 2.0

# change solid color
evenlySpacedStreamlines2D1Display.AmbientColor = [1.0, 1.0, 1.0]
evenlySpacedStreamlines2D1Display.DiffuseColor = [1.0, 1.0, 1.0]

# turn off scalar coloring
ColorBy(evenlySpacedStreamlines2D1Display, None)

# set active source
SetActiveSource(calculator2)

# show data in view
calculator2Display = Show(calculator2, renderView1, 'GeometryRepresentation')

# show color bar/color legend
calculator2Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(calculator1)

# create a new 'Evenly Spaced Streamlines 2D'
evenlySpacedStreamlines2D2 = EvenlySpacedStreamlines2D(registrationName='EvenlySpacedStreamlines2D2', Input=calculator1)
evenlySpacedStreamlines2D2.Vectors = ['POINTS', 'U_water']
evenlySpacedStreamlines2D2.StartPosition = [0.007499999832361937, -0.012450000187527621, 0.0]

# show data in view
evenlySpacedStreamlines2D2Display = Show(evenlySpacedStreamlines2D2, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
evenlySpacedStreamlines2D2Display.Representation = 'Surface'
# hide data in view
Hide(calculator1, renderView1)

# show color bar/color legend
evenlySpacedStreamlines2D2Display.SetScalarBarVisibility(renderView1, True)
# set active source
SetActiveSource(calculator1)

# show data in view
calculator1Display = Show(calculator1, renderView1, 'GeometryRepresentation')

# show color bar/color legend
calculator1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(evenlySpacedStreamlines2D2)

# turn off scalar coloring
ColorBy(evenlySpacedStreamlines2D2Display, None)

# change solid color
evenlySpacedStreamlines2D2Display.AmbientColor = [1.0, 1.0, 1.0]
evenlySpacedStreamlines2D2Display.DiffuseColor = [1.0, 1.0, 1.0]

# Properties modified on evenlySpacedStreamlines2D2Display
evenlySpacedStreamlines2D2Display.LineWidth = 2.0
evenlySpacedStreamlines2D2.IntegrationStepUnit = 'Cell Length'
evenlySpacedStreamlines2D2.SeparatingDistanceRatio = 0.2
evenlySpacedStreamlines2D2.ClosedLoopMaximumDistance = 0.0

# Rescale transfer function
u_airLUT.RescaleTransferFunction(0.0, 22.37)
# Rescale transfer function
u_airPWF.RescaleTransferFunction(0.0, 22.37)

# get color legend/bar for u_airLUT in view renderView1
u_airLUTColorBar = GetScalarBar(u_airLUT, renderView1)
u_airLUTColorBar.WindowLocation = 'AnyLocation'
u_airLUTColorBar.ComponentTitle = 'Magnitude'

# # Properties modified on u_airLUTColorBar
u_airLUTColorBar.Title = 'Uair'
u_airLUTColorBar.ScalarBarLength = color_bar_length 
u_airLUTColorBar.ScalarBarThickness = color_bar_thickness
# # Properties modified on u_airLUTColorBar
u_airLUTColorBar.Orientation = 'Vertical'
# u_airLUTColorBar.Orientation = 'Horizontal'

# Properties modified on u_airLUTColorBar
u_airLUTColorBar.TitleFontFamily = font
u_airLUTColorBar.TitleFontSize = size

# Properties modified on u_airLUTColorBar
u_airLUTColorBar.LabelFontFamily = font
u_airLUTColorBar.LabelFontSize = size
# Properties modified on u_airLUTColorBar
u_airLUTColorBar.DrawTickMarks = 1

# Properties modified on u_airLUTColorBar
u_airLUTColorBar.DrawTickLabels = 1

# Properties modified on u_airLUTColorBar
u_airLUTColorBar.Position = [0.67, 0.55]

#change interaction mode for render view
renderView1.InteractionMode = '2D'

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# Create last time step directory in post-process to save screenshots in
os.makedirs('{}/post-processing/{}'.format(os.getcwd(),last_time_step), exist_ok=True)
time_dir_to_safe = '{}/post-processing/{}'.format(os.getcwd(),last_time_step)

uSnap = '{}/velocities-and-streamlines-{}.png'.format(time_dir_to_safe, last_time_step)

# save screenshot
SaveScreenshot(uSnap, renderView1, ImageResolution=[width, height])

cmd = "sips -s dpiHeight " + str(float(DPI)) + " -s dpiWidth " + str(float(DPI)) + " " + uSnap
os.system(cmd)