#!/usr/bin/env python3

import csv
import os


DFA_dict = dict()

# open employee CSV file and create a dictionary of LDAPs (keys)
# to employee IDs (values)
with open('ldap_to_id.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        DFA_dict[row[0].lower()] = row[1]

# in the current directory, loop through the filenames and
# attempt to match LDAP, replacing with employee ID
for filename in os.listdir('.'):
    lowercase = filename.lower().strip('.png')
    for key, value in DFA_dict.items():
        if key == lowercase:
            os.rename(filename, value + '.png')
