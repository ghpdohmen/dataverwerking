class Student:
    name = None #student name
    group = None #in which group is this student?
    testResults = None

    def __init__(self,_name,_group) -> None:
        self.name = _name
        self.group = _group
        self.testResults = []
    
    def findTestResult (self,_test):
        """Checks if a specific test was taken by the student. If so, returns the test

        Args:
            _test (Test): test to check

        Returns:
            TestResult: result of the test
        """
        for _tr in self.testResults:
            if _tr.test == _test:
                return _tr
            else:
                continue
        return None