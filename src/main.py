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
#for _group in dataContainer.DataContainer.instance.groups:
#    if _group.name == "H3A":
#        groupDatasheetGenerator.generatePDF(_group)
for _student in dataContainer.DataContainer.instance.students:
    #if(_student.group.name == "H3A"):
    studentDatasheetGenerator.generatePDF(_student)