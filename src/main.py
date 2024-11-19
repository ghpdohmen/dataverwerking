from tkinter import *
from tkinter import ttk
from tkinter import Tk
from Controllers.testLoader import TestLoader
from tkinter.filedialog import askopenfilename


global klassen 
global students

Tk().withdraw()
filename = askopenfilename()

TestLoader.loadFile(filename)