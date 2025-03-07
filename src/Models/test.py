import statistics

class Test:
    name = None #string, test name
    date = None #test date
    maxPoints = 0 #max number of points on test
    nTerm = 0 #grading term
    numberOfQuestions = 0 #number of questions on test
    testResults = [] #all results of this test
    questions = [] #all questions of this test


    
    def __init__(self, _name):
        self.name = _name

    def __init__(self, _name, _date):
        self.name = _name
        self.date = _date

    def average(self):
        _data = [t.grade for t in self.testResults]
        return statistics.mean(_data)
    
    def stdev(self):
        _data = [t.grade for t in self.testResults]
        return statistics.stdev(_data)
    
    def median(self):
        _data = [t.grade for t in self.testResults]
        return statistics.median(_data)

    