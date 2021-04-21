# Imports
import math
import json
import time
import vtk

# Constants
global NUM_ROW_MAX 
NUM_ROW_MAX = 50
global NUM_COL
NUM_COL = 72
global FIRSTS_COL_HAS_FIFTY
FIRST_COL_HAS_FIFTY = 1 # 1 if true, 0 if false (ie. first column has 49 entries)
global INIT_HEIGHT
INIT_HEIGHT = 0

global PIN_CENTER_TO_CENTER
PIN_CENTER_TO_CENTER = 4
global MM_ROW_DISTANCE
MM_ROW_DISTANCE = PIN_CENTER_TO_CENTER   # y-axis distance between rows
global PIN_HOLE_DEGREE_OFFSET_RAD
PIN_HOLE_DEGREE_OFFSET_RAD = 30 * math.pi / 180  # distance between colA and colB pin centers along y
global MM_ROW_DISTANCE_AB_CENTERS
MM_ROW_DISTANCE_AB_CENTERS = PIN_CENTER_TO_CENTER * math.sin(PIN_HOLE_DEGREE_OFFSET_RAD) # distance between colA and colB pin centers along y
global COL_SPACING_X
COL_SPACING_X = PIN_CENTER_TO_CENTER*math.cos(PIN_HOLE_DEGREE_OFFSET_RAD)

global XLIM 
XLIM = math.ceil(COL_SPACING_X*NUM_COL)
global YLIM
YLIM = math.ceil(MM_ROW_DISTANCE*NUM_ROW_MAX)
global ZLIM
ZLIM = 50

global INIT_HEATING_TIME
INIT_HEATING_TIME = 60

# Global variables
global file_path
file_path = ""
global mesh
global heating_time 
heating_time = INIT_HEATING_TIME
global height_data
height_data = []

# VTK related stuff
global colors
colors = vtk.vtkNamedColors()
global renderer_for_qt
renderer_for_qt = vtk.vtkRenderer()
global iren_qt