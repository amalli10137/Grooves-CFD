# trace generated using paraview version 5.11.2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

import sys
import re
pressure_kick = sys.argv[1]

def extract_number_before_e(string):
    match = re.match(r'^\d+(?=e)', string)
    if match:
        return match.group(0)
    return None

num_for_naming = extract_number_before_e(pressure_kick)
replace_file_name = "icoFoam_" + str(num_for_naming)

#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
openfoam = OpenFOAMReader(registrationName='open.foam', FileName='/Users/amalli/Desktop/channel-cfd/pressure_sweep/cases/'+pressure_kick+'/'+replace_file_name+'/open.foam')
openfoam.MeshRegions = ['internalMesh']
openfoam.CellArrays = ['U', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
openfoamDisplay = Show(openfoam, renderView1, 'UnstructuredGridRepresentation')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# trace defaults for the display properties.
openfoamDisplay.Representation = 'Surface'
openfoamDisplay.ColorArrayName = ['POINTS', 'p']
openfoamDisplay.LookupTable = pLUT
openfoamDisplay.SelectTCoordArray = 'None'
openfoamDisplay.SelectNormalArray = 'None'
openfoamDisplay.SelectTangentArray = 'None'
openfoamDisplay.OSPRayScaleArray = 'p'
openfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
openfoamDisplay.SelectOrientationVectors = 'U'
openfoamDisplay.ScaleFactor = 0.010000000149011612
openfoamDisplay.SelectScaleArray = 'p'
openfoamDisplay.GlyphType = 'Arrow'
openfoamDisplay.GlyphTableIndexArray = 'p'
openfoamDisplay.GaussianRadius = 0.0005000000074505806
openfoamDisplay.SetScaleArray = ['POINTS', 'p']
openfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
openfoamDisplay.OpacityArray = ['POINTS', 'p']
openfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
openfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
openfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
openfoamDisplay.ScalarOpacityFunction = pPWF
openfoamDisplay.ScalarOpacityUnitDistance = 0.007434966041896619
openfoamDisplay.OpacityArrayName = ['POINTS', 'p']
openfoamDisplay.SelectInputVectors = ['POINTS', 'U']
openfoamDisplay.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
openfoamDisplay.ScaleTransferFunction.Points = [-1.448479997634422e-05, 0.0, 0.5, 0.0, 5.239505298959557e-06, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
openfoamDisplay.OpacityTransferFunction.Points = [-1.448479997634422e-05, 0.0, 0.5, 0.0, 5.239505298959557e-06, 1.0, 0.5, 0.0]

# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
openfoamDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get 2D transfer function for 'p'
pTF2D = GetTransferFunction2D('p')

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(registrationName='PlotOverLine1', Input=openfoam)
plotOverLine1.Point1 = [0.0, -0.01600000075995922, 0.0]
plotOverLine1.Point2 = [0.10000000149011612, 0.019999999552965164, 0.009999999776482582]

# Properties modified on plotOverLine1
plotOverLine1.Point1 = [0.1, 0.0, 0.005]
plotOverLine1.Point2 = [0.10000000149011612, 0.019999999552965164, 0.005]

# show data in view
plotOverLine1Display = Show(plotOverLine1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
plotOverLine1Display.Representation = 'Surface'
plotOverLine1Display.ColorArrayName = ['POINTS', 'p']
plotOverLine1Display.LookupTable = pLUT
plotOverLine1Display.SelectTCoordArray = 'None'
plotOverLine1Display.SelectNormalArray = 'None'
plotOverLine1Display.SelectTangentArray = 'None'
plotOverLine1Display.OSPRayScaleArray = 'p'
plotOverLine1Display.OSPRayScaleFunction = 'PiecewiseFunction'
plotOverLine1Display.SelectOrientationVectors = 'U'
plotOverLine1Display.ScaleFactor = 0.0019999999552965165
plotOverLine1Display.SelectScaleArray = 'p'
plotOverLine1Display.GlyphType = 'Arrow'
plotOverLine1Display.GlyphTableIndexArray = 'p'
plotOverLine1Display.GaussianRadius = 9.999999776482583e-05
plotOverLine1Display.SetScaleArray = ['POINTS', 'p']
plotOverLine1Display.ScaleTransferFunction = 'PiecewiseFunction'
plotOverLine1Display.OpacityArray = ['POINTS', 'p']
plotOverLine1Display.OpacityTransferFunction = 'PiecewiseFunction'
plotOverLine1Display.DataAxesGrid = 'GridAxesRepresentation'
plotOverLine1Display.PolarAxes = 'PolarAxesRepresentation'
plotOverLine1Display.SelectInputVectors = ['POINTS', 'U']
plotOverLine1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
plotOverLine1Display.ScaleTransferFunction.Points = [-1.448479997634422e-05, 0.0, 0.5, 0.0, -1.2949150914209895e-05, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
plotOverLine1Display.OpacityTransferFunction.Points = [-1.448479997634422e-05, 0.0, 0.5, 0.0, -1.2949150914209895e-05, 1.0, 0.5, 0.0]

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')

# show data in view
plotOverLine1Display_1 = Show(plotOverLine1, lineChartView1, 'XYChartRepresentation')

# trace defaults for the display properties.
plotOverLine1Display_1.UseIndexForXAxis = 0
plotOverLine1Display_1.XArrayName = 'arc_length'
plotOverLine1Display_1.SeriesVisibility = ['p', 'U_Magnitude']
plotOverLine1Display_1.SeriesLabel = ['arc_length', 'arc_length', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'vtkValidPointMask', 'vtkValidPointMask', 'Points_X', 'Points_X', 'Points_Y', 'Points_Y', 'Points_Z', 'Points_Z', 'Points_Magnitude', 'Points_Magnitude']
plotOverLine1Display_1.SeriesColor = ['arc_length', '0', '0', '0', 'p', '0.8899977111467154', '0.10000762951094835', '0.1100022888532845', 'U_X', '0.220004577706569', '0.4899977111467155', '0.7199969481956207', 'U_Y', '0.30000762951094834', '0.6899977111467155', '0.2899977111467155', 'U_Z', '0.6', '0.3100022888532845', '0.6399938963912413', 'U_Magnitude', '1', '0.5000076295109483', '0', 'vtkValidPointMask', '0.6500038147554742', '0.3400015259021897', '0.16000610360875867', 'Points_X', '0', '0', '0', 'Points_Y', '0.8899977111467154', '0.10000762951094835', '0.1100022888532845', 'Points_Z', '0.220004577706569', '0.4899977111467155', '0.7199969481956207', 'Points_Magnitude', '0.30000762951094834', '0.6899977111467155', '0.2899977111467155']
plotOverLine1Display_1.SeriesOpacity = ['arc_length', '1.0', 'p', '1.0', 'U_X', '1.0', 'U_Y', '1.0', 'U_Z', '1.0', 'U_Magnitude', '1.0', 'vtkValidPointMask', '1.0', 'Points_X', '1.0', 'Points_Y', '1.0', 'Points_Z', '1.0', 'Points_Magnitude', '1.0']
plotOverLine1Display_1.SeriesPlotCorner = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine1Display_1.SeriesLabelPrefix = ''
plotOverLine1Display_1.SeriesLineStyle = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine1Display_1.SeriesLineThickness = ['arc_length', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'vtkValidPointMask', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'Points_Magnitude', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['arc_length', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'vtkValidPointMask', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'Points_Magnitude', '0']
plotOverLine1Display_1.SeriesMarkerSize = ['arc_length', '4', 'p', '4', 'U_X', '4', 'U_Y', '4', 'U_Z', '4', 'U_Magnitude', '4', 'vtkValidPointMask', '4', 'Points_X', '4', 'Points_Y', '4', 'Points_Z', '4', 'Points_Magnitude', '4']

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=lineChartView1, layout=layout1, hint=0)

# Properties modified on plotOverLine1Display_1
plotOverLine1Display_1.SeriesOpacity = ['arc_length', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'vtkValidPointMask', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'Points_Magnitude', '1']
plotOverLine1Display_1.SeriesPlotCorner = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesLineStyle = ['Points_Magnitude', '1', 'Points_X', '1', 'Points_Y', '1', 'Points_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'p', '1', 'vtkValidPointMask', '1']
plotOverLine1Display_1.SeriesLineThickness = ['Points_Magnitude', '2', 'Points_X', '2', 'Points_Y', '2', 'Points_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'p', '2', 'vtkValidPointMask', '2']
plotOverLine1Display_1.SeriesMarkerStyle = ['Points_Magnitude', '0', 'Points_X', '0', 'Points_Y', '0', 'Points_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'p', '0', 'vtkValidPointMask', '0']
plotOverLine1Display_1.SeriesMarkerSize = ['Points_Magnitude', '4', 'Points_X', '4', 'Points_Y', '4', 'Points_Z', '4', 'U_Magnitude', '4', 'U_X', '4', 'U_Y', '4', 'U_Z', '4', 'arc_length', '4', 'p', '4', 'vtkValidPointMask', '4']

# update the view to ensure updated data information
lineChartView1.Update()

# split cell
layout1.SplitVertical(2, 0.5)

# set active view
SetActiveView(None)

# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
plotOverLine1Display_2 = Show(plotOverLine1, spreadSheetView1, 'SpreadSheetRepresentation')

# assign view to a particular cell in the layout
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=6)

# Properties modified on plotOverLine1Display_2
plotOverLine1Display_2.Assembly = ''

# export view
ExportView('/Users/amalli/Desktop/channel-cfd/pressure_sweep/cases/'+pressure_kick+'/uprofile_outlet.csv', view=spreadSheetView1, RealNumberNotation='Fixed')

#================================================================
# addendum: following script captures some of the application
# state to faithfully reproduce the visualization during playback
#================================================================

#--------------------------------
# saving layout sizes for layouts

# layout/tab size in pixels
layout1.SetSize(2275, 1440)

#-----------------------------------
# saving camera placements for views

# current camera placement for renderView1
renderView1.CameraPosition = [0.05000000074505806, 0.0019999993965029716, 0.21122912533538651]
renderView1.CameraFocalPoint = [0.05000000074505806, 0.0019999993965029716, 0.004999999888241291]
renderView1.CameraParallelScale = 0.05337602532055809

#--------------------------------------------
# uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).