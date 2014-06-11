#!/usr/bin/env python3

import csv
import os


DFA_dict = dict()

# open employee CSV file and create a dictionary of LDAPs (keys)
# to employee IDs (values)
with open('ldap_to_id.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        try:
            DFA_dict[row[0].lower()] = row[1]
        except Exception as e:
            print(e)

# in the current directory, loop through the filenames and
# attempt to match LDAP, replacing with employee ID
for myfile in os.listdir('.'):
    lowercase = myfile.lower()
    filename = os.path.splitext(lowercase)
    ldap = filename[0]
    for key, value in DFA_dict.items():
        if key == ldap:
            try:
                os.rename(myfile, value + '.png')
            except Exception as e:
                print(e)
