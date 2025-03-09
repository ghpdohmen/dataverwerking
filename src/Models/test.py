import statistics

class Test:
    name = None #string, test name
    date = None #test date
    version = None #gives version of the test, if applicable
    maxPoints = 0 #max number of points on test
    nTerm = 0 #grading term
    numberOfQuestions = 0 #number of questions on test
    testResults = [] #all results of this test
    questions = [] #all questions of this test


    
    def __init__(self, _name):
        self.name = _name
        self.date = None
        self.questions = []
        self.testResults = []
        self.nTerm = 0
        self.maxPoints = 0
        self.version = None
        

    def __init__(self, _name, _date):
        self.name = _name
        self.date = _date
        self.questions = []
        self.testResults = []
        self.nTerm = 0
        self.maxPoints = 0
        self.version = None

    def average(self):
        _data = [t.grade for t in self.testResults]
        return statistics.mean(_data)
    
    def stdev(self):
        _data = [t.grade for t in self.testResults]
        return statistics.stdev(_data)
    
    def median(self):
        _data = [t.grade for t in self.testResults]
        return statistics.median(_data)

    