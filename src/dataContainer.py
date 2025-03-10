class DataContainer:
    instance = None
    groups = []
    students = []
    tests = []
    teacher = "G. Dohmen"
    schoolName = "Augustinianum"
    subject = "Natuurkunde"
    logoPath = ""
    colorHex1 = "#452278"
    colorHex2 = "#FFFFFF"
    colorHex3 = "#AE9962"
    colorHex4 = "#0F4688"
    groupDatasheetTitle = "Klasgegevens"
    groupDatasheetTitle2 = "Grafiek met gemiddeldes van alle toetsen"
    groupDatasheetTitle3 = "Toetsresultaten"
    groupDatasheetGraphTitle1 = "Cijfers"
    groupDataSheetGraphTitle2 = "Moeilijkheidsgraad"
    groupDatasheetGraphTitle3 = "Type vraag"
    studentDatasheetTitle = "Leerlinggegevens"

    def __init__(self,a) -> None:
        if(DataContainer.instance):
            raise DataContainer.instance
        DataContainer.instance = self
        pass

    def findGroup(self, _name):
        """Find a specific group by name

        Args:
            _name (String): name of the group

        Returns:
            Group: either None if no group was found or the specified group
        """
        for _g in self.groups:
            if _g.name == _name:
                return _g
        return
    
    def findStudent(self, _name):
        """Find a specific student by name

        Args:
            _name (String): name of the student (first + " " + last)

        Returns:
            Student: either None if no student was found or the specified student
        """
        for _s in self.students:
            if _s.name == _name:
                return _s
        return