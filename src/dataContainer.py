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

    def __init__(self,a) -> None:
        if(DataContainer.instance):
            raise DataContainer.instance
        DataContainer.instance = self
        pass

    def findGroup(self, _name):
        for _g in self.groups:
            if _g.name == _name:
                return _g
        return