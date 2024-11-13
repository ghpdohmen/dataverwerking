class Student:
    name = None #student name
    klas = None #in which group is this student?
    testResults = None

    def __init__(self,_name,_klas) -> None:
        self.name = _name
        self.klas = _klas