import pandas as pd

from Models.mainDataContainer import mainDataContainer

class TestLoader:
    global instance


    def __init__(self) -> None:
        TestLoader.instance = self
        pass

    def loadFile(_fileName):
        _excelfile = pd.ExcelFile(_fileName)
        print(_excelfile.sheet_names)
        for _sheet in _excelfile.sheet_names:
            if(_sheet[0] == '|'):
                #if sheet name starts with |, then it's a test
                TestLoader.handleTest(pd.read_excel(_excelfile,_sheet))


    def handleTest(_testSheet):
        a = mainDataContainer()
        return 0
