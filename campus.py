#!/usr/bin/python

import requests
import getpass
from collections import namedtuple
import xmltodict
import campus_data
import ast
import sys, os
import os.path

print("")

pathname = os.path.dirname(sys.argv[0])
pathname = (os.path.abspath(pathname))
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


def real_login():
    global dist_url, district_id, username, password, app_name
    print("Your Infinite Campus:")
    district_id = input('District ID - ')
    dist_url = "https://mobile.infinitecampus.com/mobile/checkDistrict?districtCode={}".format(district_id)
    response = session.get(dist_url)
    dist = ast.literal_eval((response.text).replace(':null,',':"null",'))
    dist_url = dist['districtBaseURL']
    app_name = dist['districtAppName']
    username = str(input("  Username - "))
    password = str(getpass.getpass("  Password - "))

def save_login(user, passw, dist_id):
    global dist_url, district_id, username, password, app_name
    district_id = dist_id
    dist_url = "https://mobile.infinitecampus.com/mobile/checkDistrict?districtCode={}".format(district_id)
    response = session.get(dist_url)
    dist = ast.literal_eval((response.text).replace(':null,',':"null",'))
    dist_url = dist['districtBaseURL']
    app_name = dist['districtAppName']
    username = user
    password = passw


session = requests.session()
username = ""
password = ""
district_id = ""
dist_url = ""
app_name = ""

if os.path.exists("{}/.gitcache".format(pathname)):
    saved = input('Do you want to use the saved login?(y/n) ')
    if not saved == "y" and not saved == "n":
        print("Error: Incorrect input")
        exit()
    if saved == "y":
        login = open("{}/.gitcache".format(pathname), 'r')
        if login.mode == 'r':
            login_raw  = login.read()
            login_data = ast.literal_eval(login_raw)
            user = login_data['username']
            passw = login_data['password']
            dist_id = login_data['district_id']
            save_login(user, passw, dist_id)
    if saved == "n":
        rmlog = input('Do you want to delete existing saved login?(y/n) ')
        if not rmlog == 'y' and not rmlog == 'n':
            print("Error: Incorrect input")
            exit()
        if rmlog == "y":
            os.remove("{}/.gitcache".format(pathname))
            print("Saved login removed")
        real_login()

else:
    saved = "n"
    real_login()

"""print("Your Infinite Campus:")
district_id = input('District ID - ')
dist_url = "https://mobile.infinitecampus.com/mobile/checkDistrict?districtCode={}".format(district_id)
response = session.get(dist_url)
dist = ast.literal_eval((response.text).replace(':null,',':"null",'))
dist_url = dist['districtBaseURL']
app_name = dist['districtAppName']
username = str(input("  Username - "))
password = str(getpass.getpass("  Password - "))"""

verify_url = '{}/verify.jsp?nonBrowser=true&username={}&password={}&appName={}'.format(dist_url, username, password, app_name)
verify = session.get(verify_url)
response = verify.text
response = response.strip()
if not response == "<AUTHENTICATION>success</AUTHENTICATION>":
    print("Incorrect Username or Password:")
    print(response)
    exit()
if saved == 'n':
    saving = input("Do you want so save the login data for future sessions?(y/n) ")
    if not saving == 'y' and not saving == 'n':
        print("Error: Incorrect Input")
        exit()
    if saving == 'y':
        try:
            outFile = open('{}/.gitcache'.format(pathname),'w')
            outFile.write("{'username':'%s','password':'%s','district_id':'%s'}" % (username, password, district_id))
            outFile.close()
        except IOError as e:
            errno, strerror
            print("I/O error({0}): {1}".format(errno, strerror))

portal_url = '{}/prism?x=portal.PortalOutline&appName={}'.format(dist_url, app_name)
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
grades_url = '{}/prism?&x=portal.PortalClassbook-getClassbookForAllSections&mode=classbook&personID={}&structureID={}&calendarID={}'.format(dist_url, person_id, structure_id, calendar_id)

response = session.get(grades_url)
grades = campus_data.grade_data(response)
courses = grades.courses()

sem = str(input("\n1: Semester 1\n2: Semester 2\n3: Both Semesters\n\nPick One: (1/2/3) "))
if not sem == '1' and not sem == '2' and not sem == '3':
    print("Error: Incorrect Input")
    exit()

        
print("")

for i in courses:
    course = i['ClassbookDetail']['StudentList']['Student']['Classbook']
    final_grades = get_final_grades(course)
    if final_grades['@percentage'] == '0.0':
        final_grades['@letterGrade'] = ""
        final_grades['@formattedPercentage'] = "not available"
    if sem == '1' and course['@termName'] == 'S1':
        print("{} - {} ({})".format(course['@courseName'],final_grades['@letterGrade'],final_grades['@formattedPercentage']))
    if sem == '2' and course['@termName'] == 'S2':
        print("{} - {} ({})".format(course['@courseName'],final_grades['@letterGrade'],final_grades['@formattedPercentage']))
    if sem == '3':
        print("{} - {} ({})".format(course['@courseName'],final_grades['@letterGrade'],final_grades['@formattedPercentage']))
# print('{}\n{}\n{}'.format(verify_url, portal_url, grades_url))
