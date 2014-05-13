#!/usr/bin/env python3

import os


# in the current directory, loop through the filenames and
# attempt to match both first and last name, replacing with
# employee ID
with open('ldaps.txt', 'w') as ldaps:
    for image in os.listdir('.'):
        filename = image.strip('.png')
        ldaps.write(filename + '\n')
