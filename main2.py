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
from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from PyQt5.uic import loadUi

from main_ui_2 import Ui_MainWindow


# VTK stuff
from vedo import *

class Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        # global Ui_MainWindow
        super().__init__(parent)
        data_sc.selectFile()
        graphics_sc.stlActorConfig()
        self.setupUi(self)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())