import requests
import getpass
import xmltodict
import json
from collections import namedtuple


session = requests.session()
print("Your Infinite Campus:")
username = input("  Username - ")
password = getpass.getpass("  Password - ")
app_name = 'grossmont'
verify_url = 'https://grossmontca.infinitecampus.org/campus/verify.jsp?nonBrowser=true&username={}&password={}&appName=grossmont'.format(username,password)
verify = session.get(verify_url)
response = verify.text
response = response.strip()
if not response == "<AUTHENTICATION>success</AUTHENTICATION>":
    print("Incorrect Username or Password:")
    print(response)
    exit()
portal_url = 'https://grossmontca.infinitecampus.org/campus/prism?x=portal.PortalOutline&appName={}'.format(app_name)
portal = session.get(portal_url)
response = portal.text
response = xmltodict.parse(response)
# response = json.dumps(response)
# response = json2obj(response)
student = response['campusRoot']['PortalOutline']['Family']['Student']
person_id = student['@personID']
schedule_structure = student['Calendar']['ScheduleStructure']
structure_id = schedule_structure['@structureID']
calendar_id = schedule_structure['@calendarID']
grades_url = 'https://grossmontca.infinitecampus.org/campus/prism?&x=portal.PortalClassbook-getClassbookForAllSections&mode=classbook&personID={}&structureID={}&calendarID={}'.format(person_id, structure_id, calendar_id)

grades = session.get(grades_url)
response = grades.text
response = xmltodict.parse(response)
classes = response['campusRoot']['SectionClassbooks']['PortalClassbook']

for i in classes:
    print(i['ClassbookDetail']['StudentList']['Student']['Classbook']['@courseName'])
# print('{}\n{}\n{}'.format(verify_url, portal_url, grades_url))
