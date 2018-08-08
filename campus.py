#!/usr/bin/python

import requests
import getpass
from collections import namedtuple
from user import user
import xmltodict
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
            username = login_data['username']
            password = login_data['password']
            district_id = login_data['district_id']
    if saved == "n":
        rmlog = input('Do you want to delete existing saved login?(y/n) ')
        if not rmlog == 'y' and not rmlog == 'n':
            print("Error: Incorrect input")
            exit()
        if rmlog == "y":
            os.remove("{}/.gitcache".format(pathname))
            print("Saved login removed")
        print("Your Infinite Campus:")
        district_id = input('District ID - ')
        username = str(input("  Username - "))
        password = str(getpass.getpass("  Password - "))

else:
    saved = "n"
    print("Your Infinite Campus:")
    district_id = input('District ID - ')
    username = str(input("  Username - "))
    password = str(getpass.getpass("  Password - "))

student = user(username, password, district_id)
connect_all = student.connect_all()
connected = True
for i in connect_all[0]:
    if connected == False:
        break;
    connected = i

if connected == False:
    print(connect_all[1])
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


sem = str(input("\n1: Semester 1\n2: Semester 2\n3: Both Semesters\n\nPick One: (1/2/3) "))
if not sem == '1' and not sem == '2' and not sem == '3':
    print("Error: Incorrect Input")
    exit()
student.set_semester(sem)
grades = student.get_classes()
print("")
if grades[1] == '':
    for key, value in grades[0].items():
        print("{} - {} ({})".format(key,value[0],value[1]))

else:
    print(grades[1])
