# Imports
import math
import json
import time
import vtk

import numpy as np

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

import global_variables as gvars
import graphics_support_code as graphics_sc

# Functions
def rayCastXY(posX, posY):
    heightXY = 0
    pSource = [posX, posY, 0.0]
    pTarget = [posX, posY, 1000.0]
    obbtree = vtk.vtkOBBTree()
    obbtree.SetDataSet(gvars.mesh)
    # obbtree.SetDataSet(graphics_sc.actorStl.GetMapper().GetInputAsDataSet())
    obbtree.BuildLocator()
    pointsVTKIntersection = vtk.vtkPoints()
    code = obbtree.IntersectWithLine(pSource, pTarget, pointsVTKIntersection, None)
    pointsVTKIntersectionData = pointsVTKIntersection.GetData()
    noPointsVTKIntersection = pointsVTKIntersectionData.GetNumberOfTuples()
    pointsIntersection = []
    for idx in range(noPointsVTKIntersection):
        _tup = pointsVTKIntersectionData.GetTuple3(idx)
        pointsIntersection.append(_tup)
    ptsIntNp = np.array(pointsIntersection)

    # check if intersection points were found; otherwise heightXY is unchanged (ie. it's kept at 0)
    if pointsIntersection:
        heightXY = np.amax(ptsIntNp[:,2])
    if heightXY > gvars.ZLIM:
        heightXY = gvars.ZLIM
    # this shouldn't trigger, but included just in case
    if heightXY < 0:
        heightXY = 0
    return heightXY

def resetHeightData():
    gvars.height_data = [[gvars.INIT_HEIGHT for i in range(gvars.NUM_COL)] for j in range(gvars.NUM_ROW_MAX)]
    for i in range(gvars.NUM_COL):
        if (i+gvars.FIRST_COL_HAS_FIFTY)%2 == 0:
            gvars.height_data[gvars.NUM_ROW_MAX-1][i] = -1

def genPtCloud():
    f2name = str(int(time.time())) + "_pt_cloud.xyz"
    f2 = open(f2name, "a")
    for xNum in range(gvars.NUM_COL):
        x = xNum*gvars.COL_SPACING_X
        for yNum in range(0, gvars.NUM_ROW_MAX):
            if gvars.height_data[gvars.NUM_ROW_MAX-1][xNum] == -1:
                y = yNum*gvars.PIN_CENTER_TO_CENTER + gvars.MM_ROW_DISTANCE_AB_CENTERS
            else:
                y = yNum*gvars.PIN_CENTER_TO_CENTER
            if gvars.height_data[yNum][xNum] != -1 :
                data_str = str(x) + "," + str(y) + "," + str(gvars.height_data[yNum][xNum]) + "\n"
                f2.write(data_str)
    f2.close()
    print("Point cloud file written")

def getHeightData():
    resetHeightData()
    # loop through y-positions
    for xNum in range(gvars.NUM_COL):
        print(str(xNum) + "/" + str(gvars.NUM_COL))
        x = xNum*gvars.COL_SPACING_X
        
        # loop through x-positions
        for yNum in range(0, gvars.NUM_ROW_MAX):
          
          # check if column has 49 entries; calculate y position accordingly
          if gvars.height_data[gvars.NUM_ROW_MAX-1][xNum] == -1:
              y = yNum*gvars.PIN_CENTER_TO_CENTER + gvars.MM_ROW_DISTANCE_AB_CENTERS
          
          # column has 50 entries; calculate y position accordingly
          else:
              y = yNum*gvars.PIN_CENTER_TO_CENTER
          
          # check if the given entry's position actually exists (ie. isn't the 50th position in a 49-pin column)
          if gvars.height_data[yNum][xNum] != -1 : 
            gvars.height_data[yNum][xNum] = rayCastXY(x, y)

    genPtCloud()

def outputJson():
    # note that this doesn't check if the model is in a valid position
    json_data = {
        "pin_grid": gvars.height_data,
        "heating_time_sec": gvars.heating_time
    }
    output_file_name = str(int(time.time())) + ".json"
    with open(output_file_name, 'x') as f:
        json.dump(json_data, f)
    print("File written")

def heatTimeChanged(self, event):
    # global heating_time
    # set heating time
    placeholderVal = 0

def selectFile():
    Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
    gvars.file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
    return gvars.file_path
