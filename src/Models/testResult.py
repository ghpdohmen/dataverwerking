import random


class TestResult:
    student = None
    grade = 0
    scores = None
    test = None
    testID = None

    def __init__(self,_student,_scores, _test):
        self.student = _student
        self.scores = list(map(int, _scores))
        self.test = _test
        self.testID = _test.id
        self.grade = 0
        pass

    def calcGrade(self):
        self.totalPoints = sum(self.scores)
        self.grade = self.totalPoints/self.test.maxPoints*9 + self.test.nTerm
        #print(self.student.name +" punten: " + str(self.scores) + ", cijfer: " + str(self.grade))