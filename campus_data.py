import xmltodict


class portal_data:
    def __init__(self, portal):
        self.portal = xmltodict.parse(portal.text)

    def get_raw(self):
        return self.portal


class grade_data:
    def __init__(self, grades):
        self.raw = grades.text
        self.dict = xmltodict.parse(grades.text)

    def get_raw(self):
        return self.grades

    def dict(self):
        return self.dict

    def courses(self):
        return self.dict['campusRoot']['SectionClassbooks']['PortalClassbook']