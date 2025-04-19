class Question:
    name = None
    difficulty = None
    typeOfQuestion = None
    index = 0
    maxPoints = 0
    testID = None

    def __init__(self,_name,_difficulty,_typeOfQuestion,_maxPoints,_index,_testID) -> None:
        self.name = _name
        self.difficulty = _difficulty
        self.maxPoints = _maxPoints
        self.typeOfQuestion = _typeOfQuestion
        self.index = _index
        self.testID = _testID
        pass