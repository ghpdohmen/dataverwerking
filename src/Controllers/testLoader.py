from datetime import date
import pandas as pd


from Models.group import StudentGroup
from Models.question import Question
from Models.student import Student
from Models.test import Test
from Models.testResult import TestResult
from dataContainer import DataContainer


class TestLoader:

    def loadFile(_fileName):
        """Loads a file and starts processing it as a test

        Args:
            _fileName (String): path to the file
        """
        _excelfile = pd.ExcelFile(_fileName)
        print(_excelfile.sheet_names)
        for _sheet in _excelfile.sheet_names:
            if(_sheet[0] == '|'):
                #if sheet name starts with |, then it's a test
                TestLoader.handleTest(pd.read_excel(_excelfile,_sheet))

    def __init__(self) -> None:
        TestLoader.instance = self
        pass

    def handleTest(_testSheet):
        """_summary_
        processes a sheet containing a test into the data container.
        Args:
            _testSheet (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        #read general test data
        _testName = _testSheet.columns[1]
        _testDate = excelDateConverter(str(_testSheet.values[0][1]))
        _test = None
        _test = Test(_testName,_testDate)
        _test.nTerm = _testSheet.values[0][5]
        _test.maxPoints = _testSheet.columns[5]
        _test.numberOfQuestions = _testSheet.columns[7]
        _test.version = _testSheet.values[0][7] #load test version, might be None
        print("\n\nProcessing " + str(_test.name) + " taken at " + str(_test.date) + " with " + str(_test.numberOfQuestions) + " questions.\n")

        #read questions
        _questionLoop = 0
        while _questionLoop < _test.numberOfQuestions:
            _q = Question(_testSheet.values[1,_questionLoop+3],_testSheet.values[2,_questionLoop+3], _testSheet.values[3,_questionLoop+3], _testSheet.values[4,_questionLoop+3], _questionLoop,_test.id)
            print(str(_q.name) + " , " + str(_q.typeOfQuestion), _questionLoop)
            _test.questions.append(_q)
            _questionLoop += 1


        #read test results
        _answers = _testSheet.truncate(before=6)#create smaller dataframe
        for _row in _answers.iterrows():  #loops over all rows
            #print("\n\n\n row \n")
            _testScore = processTest([*_row[1]],_test)
        

        #debug prints
        #print(_test)
        #print(_testSheet)
        print(str(_test.average()) + " , " + str(_test.median()) + " , " + str(_test.stdev()))
        DataContainer.instance.tests.append(_test) #add to overal test list
        return 0
    
def checkIfStudentExists(_studentName):
        """_summary_
            checks if student is already in the main student array
        Args:
            _studentName (String): name of the student

        Returns:
            student: true if student already exists
        """

        
        for _student in DataContainer.instance.students:
            if(_student.name.casefold() == _studentName.casefold()):
                #print("Check " + _studentName + " passed!")
                return _student 
            else:
                #print(_student.name + " does not equal " + _studentName)
                continue #continue looping
        #print("Check " + _studentName + " failed!")
        return None

def checkIfGroupExists(_groupName):
        """_summary_
            checks if group is already in the main group array
        Args:
            _groupName (String): name of the group

        Returns:
            boolean: true if group already exists
        """
        for _group in DataContainer.instance.groups:
            if(_group.name == _groupName):
                return _group 
            else:
                continue #continue looping
        return None



def processTest(_row,_test):
        #process student
        #print(_row)
        _student = checkIfStudentExists(_row[0] + " " + _row[1])
        if (_student == None):
            #student doesn't exist, so let's create them.
            _student = addStudent(_row)
        _scores = pd.DataFrame(_row).truncate(before=3,axis=0).values
        #print(pd.DataFrame(_row).truncate(before=3,axis=0).values.tolist())
        _testScore = TestResult(_student,_scores,_test)
        _test.testResults.append(_testScore)
        _student.testResults.append(_testScore)
        _testScore.calcGrade()
        return _testScore

def addStudent(_row):
        _firstName = _row[0]
        _lastName = _row[1]
        _name = _firstName + " " + _lastName
        _groupName = _row[2]
        _group = checkIfGroupExists(_groupName)
        if(_group == None):
            #group doesn't exists, so let's create it
            _group = addGroup(_groupName)
        print("Added " + _name + " to the list.")
        _student = Student(_firstName,_lastName, _group)
        _group.students.append(_student)
        DataContainer.instance.students.append(_student)
        return _student
    
def addGroup(_name):
        _group = StudentGroup(_name)
        DataContainer.instance.groups.append(_group)
        return _group
        print("Added " + _name + " to the list.")

def excelDateConverter(_excelDate):
    """converts a string date from excel to a python date object

    Args:
        _excelDate (String): excel date in format:"yyyy-mm-dd hh:mm:ss"

    Returns:
        date: python date object
    """
    _str = _excelDate.split(" ")[0]
    _yearMonthDay = _str.split("-")
    _d = date(int(_yearMonthDay[0]),int(_yearMonthDay[1]),int(_yearMonthDay[2]))
    return _d
