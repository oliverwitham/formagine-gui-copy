import vtk

import global_variables as gvars
import data_support_code as data_sc
import graphics_support_code as graphics_sc
import time

def get_export_data():
    print(str(int(time.time())))
    gvars.iren_qt.Render()
    data_sc.getHeightData()
    data_sc.outputJson()
    print(str(int(time.time())))

def select_load_file():
    data_sc.selectFile()
    graphics_sc.stlActorConfig()
    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

def heating_time_updated(new_time):
    gvars.heating_time = int(new_time)

def rotX():
    translation = vtk.vtkTransform()
    translation.RotateX(90.0)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

def rotY():
    translation = vtk.vtkTransform()
    translation.RotateY(90.0)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

def rotZ():
    translation = vtk.vtkTransform()
    translation.RotateZ(90.0)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

def reset_sliders(transX, transY, transZ):
    global prevX
    global prevY
    global prevZ
    prevX = 0.0
    prevY = 0.0
    prevZ = 0.0
    transX.setValue(0)
    transY.setValue(0)
    transZ.setValue(0)

prevX = 0.0
def translateX(val):
    global prevX
    trans = 0.0
    trans = float(val) - prevX
    prevX = float(val)

    translation = vtk.vtkTransform()
    translation.Translate(trans, 0.0, 0.0)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

prevY = 0.0
def translateY(val):
    global prevY
    trans = 0.0
    trans = float(val) - prevY
    prevY = float(val)
    translation = vtk.vtkTransform()
    translation.Translate(0.0, trans, 0.0)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())
    graphics_sc.mapperStl.Update()

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()

prevZ = 0.0
def translateZ(val):
    global prevZ
    trans = 0.0
    trans = float(val) - prevZ
    prevZ = float(val)
    translation = vtk.vtkTransform()
    translation.Translate(0.0, 0.0, trans)

    transformFilter = vtk.vtkTransformPolyDataFilter()
    transformFilter.SetInputDataObject(gvars.mesh)
    transformFilter.SetTransform(translation)
    transformFilter.Update()
    gvars.mesh.DeepCopy(transformFilter.GetOutput())
    graphics_sc.mapperStl.Update()

    gvars.iren_qt.Render()
    gvars.iren_qt.GetRenderWindow().Render()