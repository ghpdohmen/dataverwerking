import pandas as pd


from Models.group import StudentGroup
from Models.question import Question
from Models.student import Student
from Models.test import Test
from Models.testResult import TestResult
from dataContainer import DataContainer


class TestLoader:

    def loadFile(_fileName):
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
        _testDate = _testSheet.values[0][1]
        _test = Test(_testName,_testDate)
        _test.nTerm = _testSheet.values[0][5]
        _test.maxPoints = _testSheet.columns[5]
        _test.numberOfQuestions = _testSheet.columns[7]
        print("\n\nProcessing " + str(_test.name) + " taken at " + str(_test.date) + " with " + str(_test.numberOfQuestions) + " questions.\n")

        #read questions
        _questionLoop = 0
        while _questionLoop < _test.numberOfQuestions:
            _q = Question(_testSheet.values[1,_questionLoop+3],_testSheet.values[2,_questionLoop+3], _testSheet.values[3,_questionLoop+3], _testSheet.values[4,_questionLoop+3])
            print(str(_q.name) + " , " + str(_q.typeOfQuestion))
            _questionLoop += 1


        #read test results
        _answers = _testSheet.truncate(before=6)#create smaller dataframe
        for _row in _answers.iterrows():  #loops over all rows
            #print("\n\n\n row \n")
            _testScore = processTest([*_row[1]],_test)
        

        #debug prints
        #print(_test)
        #print(_testSheet)
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
        _scores = pd.DataFrame(_row).truncate(before=3,axis=1).values.tolist()
        _testScore = TestResult(_student,_scores,_test)
        _test.testResults.append(_testScore)
        #TODO: fix this
        #_student.testResults.append(_testScore)
        _testScore.calcGrade()
        return _testScore

def addStudent(_row):
        _name = _row[0] + " " + _row[1]
        _groupName = _row[2]
        _group = checkIfGroupExists(_groupName)
        if(_group == None):
            #group doesn't exists, so let's create it
            addGroup(_groupName)
        print("Added " + _name + " to the list.")
        _student = Student(_name, _group)
        DataContainer.instance.students.append(_student)
        return 0
    
def addGroup(_name):
        _group = StudentGroup(_name)
        DataContainer.instance.groups.append(_group)
        print("Added " + _name + " to the list.")