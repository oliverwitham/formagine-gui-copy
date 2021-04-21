# Imports
import numpy as np
from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
from matplotlib.widgets import TextBox
import matplotlib as mpl
import math
import json
import time

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

# Constants
NUM_ROW_MAX = 50
NUM_COL = 75
FIRST_COL_HAS_FIFTY = 1 # 1 if true, 0 if false (ie. first column has 49 entries)
INIT_HEIGHT = 0

PIN_CENTER_TO_CENTER = 4
MM_ROW_DISTANCE = PIN_CENTER_TO_CENTER   # y-axis distance between rows
PIN_HOLE_DEGREE_OFFSET_RAD = 30 * math.pi / 180  # distance between colA and colB pin centers along y
MM_ROW_DISTANCE_AB_CENTERS = PIN_CENTER_TO_CENTER * math.sin(PIN_HOLE_DEGREE_OFFSET_RAD) # distance between colA and colB pin centers along y
COL_SPACING_X = PIN_CENTER_TO_CENTER*math.cos(PIN_HOLE_DEGREE_OFFSET_RAD)

XLIM = math.ceil(COL_SPACING_X*NUM_COL)
YLIM = math.ceil(MM_ROW_DISTANCE*NUM_ROW_MAX)
ZLIM = 50

INIT_HEATING_TIME = 60

# Global variables
file_path = ""
your_mesh = ""
prevX = 0
prevY = 0
prevZ = 0
xBox = 0
heating_time = INIT_HEATING_TIME
height_data = []

# Functions
def resetHeightData():
    global height_data
    height_data = [[INIT_HEIGHT for i in range(NUM_COL)] for j in range(NUM_ROW_MAX)]
    for i in range(NUM_COL):
        if (i+FIRST_COL_HAS_FIFTY)%2 == 0:
            height_data[NUM_ROW_MAX-1][i] = -1

def setGraphSettings():
    axes.set_xlim3d(0, XLIM)
    axes.set_ylim3d(0, YLIM)
    axes.set_zlim3d(0, ZLIM)
    axes.set_xlabel('X')
    axes.set_ylabel('Y')
    axes.set_zlabel('Z')

def drawBasePlanes():
    xx, yy = np.meshgrid(range(XLIM), range(YLIM))
    zz = xx*0
    lowSurf = axes.plot_surface(xx, yy, zz)
    lowSurf.set_facecolor('red')
    lowSurf.set_alpha(0.7)

    xx2, zz2 = np.meshgrid(range(XLIM), range(ZLIM))
    yy2 = xx2*0+YLIM
    side1Surf = axes.plot_surface(xx2, yy2, zz2)
    side1Surf.set_facecolor('red')
    side1Surf.set_alpha(0.7)

    yy3, zz3 = np.meshgrid(range(YLIM), range(ZLIM))
    xx3 = yy3*0
    side2Surf = axes.plot_surface(xx3, yy3, zz3)
    side2Surf.set_facecolor('red')
    side2Surf.set_alpha(0.7)

def loadStl():
    global your_mesh
    your_mesh = mesh.Mesh.from_file(file_path)
    drawStl(your_mesh)

def drawStl(your_mesh):
    xBox.set_text('')
    axes.clear()
    drawBasePlanes()
    poly3dthing = mplot3d.art3d.Poly3DCollection(your_mesh.vectors)
    axes.add_collection3d(poly3dthing)
    setGraphSettings()
    poly3dthing.set_edgecolor('r')

def ptInTriangle(px, py, np_vector):
    p0x = np_vector[0][0]
    p0y = np_vector[0][1]
    p1x = np_vector[1][0]
    p1y = np_vector[1][1]
    p2x = np_vector[2][0]
    p2y = np_vector[2][1]
    Area = 0.5 *(-p1y*p2x + p0y*(-p1x + p2x) + p0x*(p1y - p2y) + p1x*p2y)
    s = 1/(2*Area)*(p0y*p2x - p0x*p2y + (p2y - p0y)*px + (p0x - p2x)*py)
    t = 1/(2*Area)*(p0x*p1y - p0y*p1x + (p0y - p1y)*px + (p1x - p0x)*py)
    if (s > 0 and t > 0 and (1-s-t) > 0):
        return True
    else:
        return False

def getHeightInTri(px, py, np_vector):
    p1 = np.array([np_vector[0][0], np_vector[0][1], np_vector[0][2]])
    p2 = np.array([np_vector[1][0], np_vector[1][1], np_vector[1][2]])
    p3 = np.array([np_vector[2][0], np_vector[2][1], np_vector[2][2]])
    v1 = p3 - p1
    v2 = p2 - p1
    cp = np.cross(v1, v2)
    a,b,c = cp
    d = np.dot(cp, p3)
    #eqn of form: a*x + b*y + c*z = d
    # z = (d - a*x - b*y)/c
    height = (d - a*px - b*py)/c
    return height

def genPtCloud():
    global height_data
    f2name = str(int(time.time())) + "_pt_cloud.xyz"
    f2 = open(f2name, "a")
    for xNum in range(NUM_COL):
        x = xNum*COL_SPACING_X
        for yNum in range(0, NUM_ROW_MAX):
            if height_data[NUM_ROW_MAX-1][xNum] == -1:
                y = yNum*PIN_CENTER_TO_CENTER + MM_ROW_DISTANCE_AB_CENTERS
            else:
                y = yNum*PIN_CENTER_TO_CENTER
            if height_data[yNum][xNum] != -1 :
                data_str = str(x) + "," + str(y) + "," + str(height_data[yNum][xNum]) + "\n"
                f2.write(data_str)
    f2.close()
    print("Point cloud file written")

def getHeightData():
    global your_mesh
    global height_data
    resetHeightData()
    # axes.clear()
    # setGraphSettings()
    # loop through y-positions
    for xNum in range(NUM_COL):
        x = xNum*COL_SPACING_X
        # loop through x-positions
        # for y in range(0, MM_ROW_DISTANCE*NUM_ROW_MAX, MM_ROW_DISTANCE):
        for yNum in range(0, NUM_ROW_MAX):
          # check if column has 49 entries; calculate y position accordingly
          if height_data[NUM_ROW_MAX-1][xNum] == -1:
              y = yNum*PIN_CENTER_TO_CENTER + MM_ROW_DISTANCE_AB_CENTERS
          # column has 50 entries; calculate y position accordingly
          else:
              y = yNum*PIN_CENTER_TO_CENTER
          # check if the given entry's position actually exists (ie. isn't the 50th position in a 49-pin column)
          if height_data[yNum][xNum] != -1 :
              # loop through all vectors
              for vec in range(int(your_mesh.vectors.size/9)):
                  # check if point is in triangle
                  if ptInTriangle(x, y, your_mesh.vectors[vec]) == True:
                      tmpHeight = getHeightInTri(x, y, your_mesh.vectors[vec])
                      # check if height is positive and greater than existing height for given position / entry
                      if tmpHeight > 0 and tmpHeight > height_data[yNum][xNum]:
                          if tmpHeight > ZLIM:
                              tmpHeight = ZLIM
                          height_data[yNum][xNum] = tmpHeight
                        #   axes.scatter(x,y,tmpHeight, color='b') # there be monsters if you uncomment this
    genPtCloud()

# Button func's
class ButtonCalls():
    def rotX(self, event):
        global your_mesh
        your_mesh.rotate([-0.5, 0.0, 0.0], math.radians(90), your_mesh.get_mass_properties()[1])
        drawStl(your_mesh)

    def rotY(self, event):
        global your_mesh
        your_mesh.rotate([0.0, 0.5, 0.0], math.radians(90), your_mesh.get_mass_properties()[1])
        drawStl(your_mesh)

    def rotZ(self, event):
        global your_mesh
        your_mesh.rotate([0.0, 0.0, 0.5], math.radians(90), your_mesh.get_mass_properties()[1])
        drawStl(your_mesh)

    def shiftX(self, event):
        global your_mesh
        global prevX
        your_mesh.translate([bSliderX.val-prevX, 0, 0])
        drawStl(your_mesh)
        prevX = bSliderX.val

    def shiftY(self, event):
        global your_mesh
        global prevY
        your_mesh.translate([0, bSliderY.val-prevY, 0])
        drawStl(your_mesh)
        prevY = bSliderY.val

    def shiftZ(self, event):
        global your_mesh
        global prevZ
        your_mesh.translate([0, 0, bSliderZ.val-prevZ])
        drawStl(your_mesh)
        prevZ = bSliderZ.val

    def resetSliders(self, event):
        global prevX
        global prevY
        global prevZ
        prevX = 0
        prevY = 0
        prevZ = 0
        bSliderX.set_val(0)
        bSliderY.set_val(0)
        bSliderZ.set_val(0)

    def btn2(self, event):
        print("btn2")

    def btnFile(self, event):
        global file_path
        Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
        file_path = askopenfilename() # show an "Open" dialog box and return the path to the selected file
        # print(file_path)

    def openStl(self, event):
        loadStl()

    def getDataModel(self, event):
        global your_mesh
        # print(your_mesh.vectors)
        # axes.scatter(100,100,50, color='b')
        getHeightData()
        print("Heights retrieved")
        # lastElement = your_mesh.vectors.size/9-1

    def validatePosition(self, event):
        global your_mesh
        # [vector][row][column], starting at 0 for each
        # print(your_mesh.vectors[0][2][1])
        m2 = your_mesh.vectors
        xVals = m2[0:,0:,0]
        yVals = m2[0:,0:,1]
        zVals = m2[0:,0:,2]
        withinBounds = False
        maxX = np.amax(xVals)
        minX = np.amin(xVals)
        maxY = np.amax(yVals)
        minY = np.amin(yVals)
        maxZ = np.amax(zVals)
        minZ = np.amin(zVals)
        if (maxX < XLIM and minX >= 0 and maxY < YLIM and minY >= 0 and maxZ < ZLIM and minZ >= 0):
            withinBounds = True 
        if (withinBounds):
            xBox.set_text("Boundaries respected")
        else:
            xBox.set_text("Error: model outside boundaries")
        # maxX = np.amax(xVals) if (np.amax(xVals) > abs(np.amin(xVals))) else abs(np.amin(xVals))
        
        # lastEntry = your_mesh.vectors.size/9-1
        # print(your_mesh.vectors[int(lastEntry)][1][0])
        
        # maxPos = np.amax(your_mesh.vectors)

        # print(maxPos)
        # print(m2)        
        # print("\n")
        # print(your_mesh.vectors.size)

    def output(self, event):
        # TODO: this doesn't check if the model is in a valid position. should it? eh
        global height_data
        global heating_time
        json_data = {
            "pin_grid": height_data,
            "heating_time_sec": heating_time
        }
        output_file_name = str(int(time.time())) + ".json"
        with open(output_file_name, 'x') as f:
            json.dump(json_data, f)
        print("File written")

    def heatTimeChanged(self, event):
        global heating_time
        heating_time = int(bTextHeatTime.text)

# Create a new plot
mpl.rcParams['toolbar'] = 'None'
figure = plt.figure('Computer Model Processor - Formagine Inc.', figsize=(16,9))
axes = mplot3d.Axes3D(figure)
axes.set_box_aspect((XLIM,YLIM,ZLIM))
setGraphSettings()
plt.Figure()

# Button positioning
pos01 = plt.axes([0, 0.1, 0.1, 0.075])
pos02 = plt.axes([0.11, 0.1, 0.1, 0.075])
pos03 = plt.axes([0.22, 0.1, 0.1, 0.075])
pos04 = plt.axes([0.33, 0.1, 0.1, 0.075])
pos05 = plt.axes([0.44, 0.1, 0.1, 0.075])
pos06 = plt.axes([0.55, 0.1, 0.1, 0.075])
pos11 = plt.axes([0.01, 0.0, 0.1, 0.075])
pos12 = plt.axes([0.14, 0.0, 0.1, 0.075])
pos13 = plt.axes([0.28, 0.0, 0.1, 0.075])
pos14 = plt.axes([0.39, 0.0, 0.1, 0.075])
pos15 = plt.axes([0.5, 0.0, 0.1, 0.075])
pos16 = plt.axes([0.61, 0.0, 0.1, 0.075])
pos17 = plt.axes([0.79, 0.0, 0.04, 0.075])

# Button usage
BtnCalls = ButtonCalls()

bRotX = Button(pos01, 'RotX')
bRotX.on_clicked(BtnCalls.rotX)

bRotY = Button(pos02, 'RotY')
bRotY.on_clicked(BtnCalls.rotY)

bRotZ = Button(pos03, 'RotZ')
bRotZ.on_clicked(BtnCalls.rotZ)

bGetFile = Button(pos04, 'File')
bGetFile.on_clicked(BtnCalls.btnFile)

bOpenFile = Button(pos05, 'Open')
bOpenFile.on_clicked(BtnCalls.openStl)

bOutput = Button(pos06, 'Output')
bOutput.on_clicked(BtnCalls.output)

bSliderX = Slider(pos11, 'X', valmin=-300, valmax=300, valinit=0, valstep=1)
bSliderX.valtext.set_visible(False)
bSliderX.vline.set_visible(False)
bSliderX.on_changed(BtnCalls.shiftX)

bSliderY = Slider(pos12, 'Y', valmin=-400, valmax=400, valinit=0, valstep=1)
bSliderY.valtext.set_visible(False)
bSliderY.vline.set_visible(False)
bSliderY.on_changed(BtnCalls.shiftY)

bSliderZ = Slider(pos13, 'Z', valmin=-100, valmax=100, valinit=0, valstep=0.5)
bSliderZ.valtext.set_visible(False)
bSliderZ.vline.set_visible(False)
bSliderZ.on_changed(BtnCalls.shiftZ)

bResetSlider = Button(pos14, 'Reset Sliders')
bResetSlider.on_clicked(BtnCalls.resetSliders)

bValidatePos = Button(pos15, 'Validate Pos.')
bValidatePos.on_clicked(BtnCalls.validatePosition)

bGetData = Button(pos16, 'Get Data')
bGetData.on_clicked(BtnCalls.getDataModel)

bTextHeatTime = TextBox(pos17, 'Heating Time (s)', initial=INIT_HEATING_TIME)
bTextHeatTime.on_submit(BtnCalls.heatTimeChanged)

# Set height data
resetHeightData()

# Show the plot to the screen
drawBasePlanes()
xBox = plt.annotate('', [0.5, 0.075], xycoords='figure fraction', size=12)
plt.show()
