# Imports
import math
import json
import time
import vtk

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import global_variables as gvars
import data_support_code as data_sc
import graphics_support_code as graphics_sc

# PyQt stuff
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

# VTK stuff
from vedo import *
readerSTL = ""
mapper = ""

def loadSTL(filenameSTL):
    global readerSTL

    readerSTL = vtk.vtkSTLReader()
    readerSTL.SetFileName(filenameSTL)
    # 'update' the reader i.e. read the .stl file
    readerSTL.Update()
    polydata = readerSTL.GetOutput()
    # If there are no points in 'vtkPolyData' something went wrong
    if polydata.GetNumberOfPoints() == 0:
        raise ValueError("No point data could be loaded from '" + filenameSTL)
        return None
    return polydata

# Program execution
data_sc.selectFile()
gvars.mesh = loadSTL(gvars.file_path)

# Create mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(readerSTL.GetOutputPort())

# Create actor
actor = vtk.vtkActor()
actor.SetMapper(mapper)
# actor.SetPosition(200,200,1)

# Get height data, and export to JSON
# data_sc.getHeightData()
# data_sc.outputJson()

def addActors(rendererIn):
    # Show model
    rendererIn.AddActor(actor)
    # Show axes
    rendererIn.AddActor(graphics_sc.axes)
    # Show base planes
    rendererIn.AddActor(graphics_sc.actorPbot)
    rendererIn.AddActor(graphics_sc.actorPside1)
    rendererIn.AddActor(graphics_sc.actorPside2)

class MainWindow(QtWidgets.QMainWindow):
 
    def __init__(self, parent = None):
        QtWidgets.QMainWindow.__init__(self, parent)
 
        self.frame = QtWidgets.QFrame()
 
        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtk.vtkRenderer()
        self.ren.SetBackground(gvars.colors.GetColor3d('SlateGray'))
        self.ren.ResetCamera()

        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        addActors(self.ren)
 
        self.frame.setLayout(self.vl)
        self.setCentralWidget(self.frame)
 
        self.show()
        self.iren.Initialize()
 
if __name__ == "__main__":
 
    app = QtWidgets.QApplication(sys.argv)
 
    window = MainWindow()
    window.setWindowTitle("Computer GUI - Formagine")
    window.resize(1600,900)

    sys.exit(app.exec_())

