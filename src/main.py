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
#    groupDatasheetGenerator.generatePDF(_group)
#for _student in dataContainer.DataContainer.instance.students:
#    studentDatasheetGenerator.generatePDF(_student)
studentDatasheetGenerator.generatePDF(dataContainer.DataContainer.instance.findStudent("Daan van Och"))