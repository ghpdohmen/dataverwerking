class Student:
    name = None #student name
    group = None #in which group is this student?
    testResults = None

    def __init__(self,_name,_group) -> None:
        self.name = _name
        self.group = _group
        self.testResults = []