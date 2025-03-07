from tkinter import *
from tkinter import Tk
from Controllers.testLoader import TestLoader
from tkinter.filedialog import askopenfilename

from Viewers.PDFGenerator import groupDatasheetGenerator
import dataContainer


_data = dataContainer.DataContainer(1)
Tk().withdraw()
filename = askopenfilename()

TestLoader.loadFile(filename)
groupDatasheetGenerator.generatePDF(dataContainer.DataContainer.instance.findGroup("G2A"))
