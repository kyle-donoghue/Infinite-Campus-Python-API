import requests, ast, xmltodict, time

class user:
    def __init__(self, username, password, dist_id):
        self.username = username
        self.password = password
        self.dist_id = dist_id
        self.connected_session = [None] * 2
        self.connected_grades = [None] * 2
        self.connected_person = [None] * 2
        self.semester = '3'
        self.session = requests.session()


    def connect_session(self):
        district_id = self.dist_id
        dist_url = "https://mobile.infinitecampus.com/mobile/checkDistrict?districtCode={}".format(district_id)
        time.sleep(0.1)
        response = self.session.get(dist_url)
        try:
            dist = ast.literal_eval((response.text).replace(':null,',':"null",'))
        except Exception as e:
            self.connected_session = False, "Incorrect District ID"
        else:
            self.dist_url = dist['districtBaseURL']
            self.app_name = dist['districtAppName']
            verify_url = '{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}'.format(self.dist_url, self.username, self.password, self.app_name)
            verify = self.session.get(verify_url)
            response = verify.text
            response = response.strip()
            if not response == "<AUTHENTICATION>success</AUTHENTICATION>":
                self.connected_session = False, response
            else:
                self.connected_session = True, ''
        return self.connected_session

    def connect_grades(self):
        try:
            self.person_id
            self.structure_id
            self.calendar_id
        except NameError:
            self.connected_grades = False, "No student variables found... Please run the connect_portal() command"
        else:
            if self.connected_person[0]:
                self.grades_url = '{}/prism?&x=portal.PortalClassbook-getClassbookForAllSections&mode=classbook&personID={}&structureID={}&calendarID={}'.format(self.dist_url, self.person_id, self.structure_id, self.calendar_id)
                time.sleep(0.1)
                response = self.session.get(self.grades_url)
                self.grades = xmltodict.parse(response.text)
                self.xml_grades = str(response.text)
                self.connected_grades = True, ''
            else:
                self.connected_grades = False, self.connected_person[1]
        return self.connected_grades

    def connect_portal(self):
        try:
            self.connected_session
        except NameError:
            self.connected_person = False, "No session found... Please run the connect_session() command"
        else:
            if self.connected_session[0]:
                portal_url = '{}/prism?x=portal.PortalOutline&appName={}'.format(self.dist_url, self.app_name)
                time.sleep(0.1)
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
                self.connected_person = True, ''
            else:
                self.connected_person = False, self.connected_session[1]
        return self.connected_person

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

    def raw_xml_grades(self):
        error = ""
        grades = ""
        try:
            self.connected_grades
        except NameError:
            error = "No grades found... Please run the connect_grade() command"
        else:
            grades = self.xml_grades
        return grades, error

    def connect_all(self):
        success = []
        errors = []
        session = [None] * 2
        portal = [None] * 2
        grades = [None] * 2
        session = self.connect_session()
        if session[0]:
            portal = self.connect_portal()
            if portal[0]:
                grades = self.connect_grades()
        success.extend((session[0], portal[0], grades[0]))
        errors.extend((session[1], portal[1], grades[1]))
        return success, errors

    def get_final_grades(course):
        tasks = course['tasks']['ClassbookTask']
        if len(tasks) == 29:
            return tasks
        for task in tasks:
            if task['@name'] == 'Final Grades':
                return task
                break
        print("Error: Final Grades not found")
        exit()

    def set_semester(self, sem):
        self.semester = sem

    def get_classes(self):
        total = {}
        errors = ""
        courses = self.grades['campusRoot']['SectionClassbooks']['PortalClassbook']
        sem = self.semester
        for i in courses:
            course = i['ClassbookDetail']['StudentList']['Student']['Classbook']
            # print(course)
           #  final_grades = self.get_final_grades(course)
            tasks = course['tasks']['ClassbookTask']
            if len(tasks) == 29:
                final_grades = tasks
            else:
                for task in tasks:
                    if task['@name'] == 'Final Grades':
                        final_grades = task
                        break
            if final_grades['@percentage'] == '0.0':
                final_grades['@letterGrade'] = ""
                final_grades['@formattedPercentage'] = "not available"
            if sem == '1' and course['@termName'] == 'S1':
                total[course['@courseName']] = [final_grades['@letterGrade'],final_grades['@formattedPercentage']]
            if sem == '2' and course['@termName'] == 'S2':
                total[course['@courseName']] = [final_grades['@letterGrade'],final_grades['@formattedPercentage']]
            if sem == '3':
                total[course['@courseName']] = [final_grades['@letterGrade'],final_grades['@formattedPercentage']]
        return total, errors
