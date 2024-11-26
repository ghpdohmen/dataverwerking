class DataContainer:
    instance = None
    groups = []
    students = []

    def __init__(self,a) -> None:
        if(DataContainer.instance):
            raise DataContainer.instance
        DataContainer.instance = self
        pass