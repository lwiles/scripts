#!/usr/bin/env python3

import csv
import os


DFA_dict = dict()

# open employee CSV file and create a dictionary of IDs (keys)
# to Firstname, Lastname tuple (values)
with open('employees_and_ids.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=',')
    for row in csvreader:
        DFA_dict[row[2]] = (row[1].lower(), row[0].lower())

# in the current directory, loop through the filenames and
# attempt to match both first and last name, replacing with
# employee ID
for filename in os.listdir('.'):
    lowercase = filename.lower()
    for key, value in DFA_dict.items():
        if value[0] in lowercase and value[1] in lowercase:
            os.rename(filename, key + '.jpg')
