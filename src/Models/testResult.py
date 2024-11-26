


import random


class TestResult:
    student = None
    grade = 0
    scores = None
    test = None

    def __init__(self,_student,_scores, _test):
        self.student = _student
        self.scores = _scores
        self.test = _test
        pass

    def calcGrade(self):
        #TODO: implement grade calculations
        self.grade = random.random()*10
        print(self.grade)