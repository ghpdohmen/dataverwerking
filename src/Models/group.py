class StudentGroup:
    name = ''
    students = []

    def __init__(self, _name) -> None:
        self.name = _name
        pass

    def testAverage(self,_test):
        """calculates average grade of this group for a test

        Args:
            _test (test): test to check
        """
        i = 0
        totalGrades = 0
        for s in self.students:
            for tr in s.testResults:
                if  (tr.test.name == _test.name):
                    i += 1
                    totalGrades += tr.grade
        if (i == 0):
            return
        
        return totalGrades/i

        