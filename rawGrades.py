#!/usr/bin/env python

import sys, getopt, os, ast
from user import user

inputfile = ''
outputfile = ''
xml = False
form = False
try:
    opts, args = getopt.getopt(sys.argv[1:],"hsxgu:p:i:",["username=","password=","district-id="])
except getopt.GetoptError:
    print('rawGrades.py -u <username> -p <password> -i <district-id> -s <optional: uses existing save file> -x <optional: spits out xml instead of default dictionary)> -g <optional: prints out formatted grades>')
    exit()
if len(opts) == 0:
    print('rawGrades.py -u <username> -p <password> -i <district-id> -s <optional: uses existing save file> -x <optional: spits out xml instead of default dictionary)> -g <optional: prints out formatted grades>')
    exit()
for opt, arg in opts:
    if opt == '-h':
        print('rawGrades.py -u <username> -p <password> -i <district-id>')
        sys.exit()
    elif opt == '-s':
        pathname = os.path.dirname(sys.argv[0])
        pathname = (os.path.abspath(pathname))
        if os.path.isfile("{}/.gitcache".format(pathname)):
            login = open("{}/.gitcache".format(pathname), 'r')
            if login.mode == 'r':
                login_raw  = login.read()
                login_data = ast.literal_eval(login_raw)
                username = login_data['username']
                password = login_data['password']
                dist_id = login_data['district_id']
        else:
            print("No saved login found... Please create one with campus.py")
            exit()
    elif opt == '-x':
        xml = True
    elif opt == '-g':
        form = True
    elif opt in ("-u", "--username"):
        username = str(arg)
    elif opt in ("-p", "--password"):
        password = str(arg)
    elif opt in ("-i", "--district-id"):
        dist_id = str(arg)
student = user(username, password, dist_id)
"""session = student.connect_session()
portal = student.connect_portal()
grades = student.connect_grades()"""
connect_all = student.connect_all()
connected = True
for i in connect_all[0]:
    if connected == False:
        break;
    connected = i

if connected == False:
    print(connect_all[1])
    exit()

if form:
    grades = student.get_classes()

else:
    if xml:
        grades = student.raw_xml_grades()
    if not xml:
        grades = student.raw_grades()

if grades[1] == '':
    print(grades[0])

else:
    print(grades[1])
