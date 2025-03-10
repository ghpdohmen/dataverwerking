from tkinter import *
from tkinter import Tk
from Controllers.testLoader import TestLoader
from tkinter.filedialog import askopenfilename

from Viewers.PDFGenerator import groupDatasheetGenerator, studentDatasheetGenerator
import dataContainer


_data = dataContainer.DataContainer(1)
Tk().withdraw()
filename = askopenfilename()

TestLoader.loadFile(filename)
groupDatasheetGenerator.generatePDF(dataContainer.DataContainer.instance.findGroup("G2A"))
for _student in dataContainer.DataContainer.instance.students:
    studentDatasheetGenerator.generatePDF(_student)
