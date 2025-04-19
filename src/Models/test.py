from datetime import date
import statistics

class Test:
    name = None #string, test name
    date = None #test date
    id = None #test ID
    version = None #gives version of the test, if applicable
    maxPoints = 0 #max number of points on test
    nTerm = 0 #grading term
    numberOfQuestions = 0 #number of questions on test
    testResults = [] #all results of this test
    questions = [] #all questions of this test


    
    def __init__(self, _name):
        self.name = _name
        self.date = None
        self.id = _name.replace(" ","")
        self.questions = []
        self.testResults = []
        self.nTerm = 0
        self.maxPoints = 0
        self.version = None
        

    def __init__(self, _name, _date):
        self.name = _name
        self.date = _date
        self.id = _name.replace(" ","") + _date.isoformat()
        self.questions = []
        self.testResults = []
        self.nTerm = 0
        self.maxPoints = 0
        self.version = None

    def average(self):
        """Calculates the average grade of the test

        Returns:
            float: mean of all results
        """
        _data = [t.grade for t in self.testResults]
        return statistics.mean(_data)
    
    def stdev(self):
        """Calculates the standard deviation of all test grades

        Returns:
            float: stdev
        """
        _data = [t.grade for t in self.testResults]
        return statistics.stdev(_data)
    
    def median(self):
        """Calculates the median of all test grades

        Returns:
            float: median
        """
        _data = [t.grade for t in self.testResults]
        return statistics.median(_data)

    