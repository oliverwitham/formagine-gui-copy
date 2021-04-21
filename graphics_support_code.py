# Imports
import math
import json
import time
import vtk

import global_variables as gvars
import data_support_code as data_sc

# Globals
global XLIM
global YLIM
global ZLIM
global colors

# Axes
transformAxes = vtk.vtkTransform()
transformAxes.Translate(0.0, 0.0, 0.0)
axes = vtk.vtkAxesActor()
axes.SetTotalLength(gvars.XLIM, gvars.YLIM, gvars.ZLIM)
axes.SetNormalizedTipLength(0,0,0)
axes.SetUserTransform(transformAxes)
axes.SetXAxisLabelText('X')
axes.SetYAxisLabelText('Y')
axes.SetZAxisLabelText('Z')

# Base plane - bottom
pointsPbot = vtk.vtkPoints()
pointsPbot.InsertNextPoint(0.0,0.0,0.0)
pointsPbot.InsertNextPoint(gvars.XLIM,0.0,0.0)
pointsPbot.InsertNextPoint(gvars.XLIM,gvars.YLIM,0.0)
pointsPbot.InsertNextPoint(0.0,gvars.YLIM,0.0)
polygonPbot = vtk.vtkPolygon()
polygonPbot.GetPointIds().SetNumberOfIds(4)
polygonPbot.GetPointIds().SetId(0, 0)
polygonPbot.GetPointIds().SetId(1, 1)
polygonPbot.GetPointIds().SetId(2, 2)
polygonPbot.GetPointIds().SetId(3, 3)

polygonPlanes = vtk.vtkCellArray()
polygonPlanes.InsertNextCell(polygonPbot)

polygonPolyDataPbot = vtk.vtkPolyData()
polygonPolyDataPbot.SetPoints(pointsPbot)
polygonPolyDataPbot.SetPolys(polygonPlanes)

mapperPbot = vtk.vtkPolyDataMapper()
mapperPbot.SetInputData(polygonPolyDataPbot)

actorPbot = vtk.vtkActor()
actorPbot.SetMapper(mapperPbot)
actorPbot.GetProperty().SetColor(gvars.colors.GetColor3d('Red'))

# Base plane - side 1
pointsPside1 = vtk.vtkPoints()
pointsPside1.InsertNextPoint(0.0,0.0,0.0)
pointsPside1.InsertNextPoint(gvars.XLIM,0.0,0.0)
pointsPside1.InsertNextPoint(gvars.XLIM,0.0,gvars.ZLIM)
pointsPside1.InsertNextPoint(0.0,0.0,gvars.ZLIM)
polygonPside1 = vtk.vtkPolygon()
polygonPside1.GetPointIds().SetNumberOfIds(4)
polygonPside1.GetPointIds().SetId(0, 0)
polygonPside1.GetPointIds().SetId(1, 1)
polygonPside1.GetPointIds().SetId(2, 2)
polygonPside1.GetPointIds().SetId(3, 3)

polygonPlanesPside1 = vtk.vtkCellArray()
polygonPlanesPside1.InsertNextCell(polygonPside1)

polygonPolyDataPside1 = vtk.vtkPolyData()
polygonPolyDataPside1.SetPoints(pointsPside1)
polygonPolyDataPside1.SetPolys(polygonPlanesPside1)

mapperPside1 = vtk.vtkPolyDataMapper()
mapperPside1.SetInputData(polygonPolyDataPside1)

actorPside1 = vtk.vtkActor()
actorPside1.SetMapper(mapperPside1)
actorPside1.GetProperty().SetColor(gvars.colors.GetColor3d('Red'))

# Base plane - side 2
pointsPside2 = vtk.vtkPoints()
pointsPside2.InsertNextPoint(0.0,0.0,0.0)
pointsPside2.InsertNextPoint(0.0,gvars.YLIM,0.0)
pointsPside2.InsertNextPoint(0.0,gvars.YLIM,gvars.ZLIM)
pointsPside2.InsertNextPoint(0.0,0.0,gvars.ZLIM)
polygonPside2 = vtk.vtkPolygon()
polygonPside2.GetPointIds().SetNumberOfIds(4)
polygonPside2.GetPointIds().SetId(0, 0)
polygonPside2.GetPointIds().SetId(1, 1)
polygonPside2.GetPointIds().SetId(2, 2)
polygonPside2.GetPointIds().SetId(3, 3)

polygonPlanesPside2 = vtk.vtkCellArray()
polygonPlanesPside2.InsertNextCell(polygonPside2)

polygonPolyDataPside2 = vtk.vtkPolyData()
polygonPolyDataPside2.SetPoints(pointsPside2)
polygonPolyDataPside2.SetPolys(polygonPlanesPside2)

mapperPside2 = vtk.vtkPolyDataMapper()
mapperPside2.SetInputData(polygonPolyDataPside2)

actorPside2 = vtk.vtkActor()
actorPside2.SetMapper(mapperPside2)
actorPside2.GetProperty().SetColor(gvars.colors.GetColor3d('Red'))

# Set up STL actor
actorStl = ""
global mapperStl
mapperStl = vtk.vtkPolyDataMapper()
global polydata
def stlActorConfig():
    global actorStl
    global polydata
    readerSTL = vtk.vtkSTLReader()
    readerSTL.SetFileName(gvars.file_path)
    # 'update' the reader i.e. read the .stl file
    readerSTL.Update()
    polydata = readerSTL.GetOutput()
    # If there are no points in 'vtkPolyData' something went wrong
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError("No point data could be loaded from '" + gvars.file_path)
    # mapperStl = vtk.vtkPolyDataMapper()
    mapperStl.SetInputConnection(readerSTL.GetOutputPort())
    gvars.mesh = polydata
    actorStl = vtk.vtkActor()
    actorStl.SetMapper(mapperStl)

# Add actors
def addActors(rendererIn):
    # Show model
    rendererIn.AddActor(actorStl)
    # Show axes
    rendererIn.AddActor(axes)
    # Show base planes
    rendererIn.AddActor(actorPbot)
    rendererIn.AddActor(actorPside1)
    rendererIn.AddActor(actorPside2)

# Print 2 points
# points = vtk.vtkPoints()
# numPts = 2
# pSource = [0.0, 0.0, 0.0]
# pTarget = [1000.0, 0.0, 0.0]
# ptVertices = vtk.vtkCellArray()
# pid = [0]*numPts
# pid[0] = points.InsertNextPoint(pSource)
# pid[1] = points.InsertNextPoint(pTarget)
# ptVertices.InsertNextCell(2, pid)

# pointsData = vtk.vtkPolyData()
# pointsData.SetPoints(points)
# pointsData.SetVerts(ptVertices)

# mapperPts = vtk.vtkPolyDataMapper()
# mapperPts.SetInputData(pointsData)

# actorPt = vtk.vtkActor()
# actorPt.SetMapper(mapperPts)
# actorPt.GetProperty().SetColor(gvars.colors.GetColor3d('Chartreuse'))
# actorPt.GetProperty().SetPointSize(4)
# ren.AddActor(actorPt)
