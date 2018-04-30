import requests, ast, xmltodict

class user:
    def __init__(self, username, password, dist_id):
        self.username = username
        self.password = password
        self.dist_id = dist_id
        self.connected_session = False
        self.connected_grades = False
        self.connected_person = False
        self.session = requests.session()

    
    def connect_session(self):
        error = ""
        district_id = self.dist_id
        dist_url = "https://mobile.infinitecampus.com/mobile/checkDistrict?districtCode={}".format(district_id)
        response = self.session.get(dist_url)
        dist = ast.literal_eval((response.text).replace(':null,',':"null",'))
        self.dist_url = dist['districtBaseURL']
        self.app_name = dist['districtAppName']
        verify_url = '{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}'.format(self.dist_url, self.username, self.password, self.app_name)
        verify = self.session.get(verify_url)
        response = verify.text
        response = response.strip()
        if not response == "<AUTHENTICATION>success</AUTHENTICATION>":
            error = response
            self.connected_session = False
        else:
            self.connected_session = True
        return self.connected_session, error
    
    def connect_grades(self):
        error = ""
        try:
            self.person_id
            self.structure_id
            self.calendar_id
        except NameError:
            error = "No student variables found... Please run the connect_portal() command"
            self.connected_grades = False
        else:
            self.grades_url = '{}/prism?&x=portal.PortalClassbook-getClassbookForAllSections&mode=classbook&personID={}&structureID={}&calendarID={}'.format(self.dist_url, self.person_id, self.structure_id, self.calendar_id)
            response = self.session.get(self.grades_url)
            self.grades = xmltodict.parse(response.text)
            self.connected_grades = True
        return self.connected_grades, error
    
    def connect_portal(self):
        error = ""
        try:
            self.connected_session
        except NameError:
            error = "No session found... Please run the connect_session() command"
            self.connected_person = False
        else:
            portal_url = '{}/prism?x=portal.PortalOutline&appName={}'.format(self.dist_url, self.app_name)
            portal = self.session.get(portal_url)
            response = portal.text
            self.portal = xmltodict.parse(response)
            # response = json.dumps(response)
            # response = json2obj(response)
            student = self.portal['campusRoot']['PortalOutline']['Family']['Student']
            self.person_id = student['@personID']
            schedule_structure = student['Calendar']['ScheduleStructure']
            self.structure_id = schedule_structure['@structureID']
            self.calendar_id = schedule_structure['@calendarID']
            self.connected_person = True
        return self.connected_person, error
    
    def raw_grades(self):
        error = ""
        grades = ""
        try:
            self.connected_grades
        except NameError:
            error = "No grades found... Please run the connect_grade() command"
        else:
            grades = self.grades
        return grades, error
    
    def connect_all(self):
        success = []
        errors = []
        session = self.connect_session()
        portal = self.connect_portal()
        grades = self.connect_grades()
        success.extend((session[0], portal[0], grades[0]))
        errors.extend((session[1], portal[1], grades[1]))
        return success, errors
        