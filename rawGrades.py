#!/usr/bin/python

import sys, getopt, os, ast
from user import user

inputfile = ''
outputfile = ''
try:
    opts, args = getopt.getopt(sys.argv[1:],"hcu:p:i:",["username=","password=","district-id="])
except getopt.GetoptError:
    print('rawGrades.py -u <username> -p <password> -i <district-id> -c <optional: uses existing save file>')
    exit()
if len(opts) == 0:
    print('rawGrades.py -u <username> -p <password> -i <district-id> -c <optional: uses existing save file>')
    exit()
for opt, arg in opts:
    if opt == '-h':
        print('rawGrades.py -u <username> -p <password> -i <district-id>')
        sys.exit()
    elif opt == '-c':
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
# if session[0] and portal[0] and grades[0]:
#     print("Everything connected successfully")
# else:
#     print("ERRORS:\nsession: {}\nportal: {}\ngrades: {}".format(session, portal, grades))
connected = True
for i in connect_all[0]:
    if connected == False:
        break;
    connected = i

if connected == False:
    print(connect_all[1])
    exit()
    
grades = student.raw_grades()

if grades[1] == '':
    print(grades[0])

else:
    print(grades[1])