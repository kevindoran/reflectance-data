#!/bin/python

import sys


"""Fix the csv formatting issues of the dataset's csv file."""


with open(sys.argv[1], 'r') as f1:
    no_spaces = f1.read().replace(' ,', ',')
    no_spaces = nospaces.read().replace('780 ', '780')


with open(sys.argv[2], 'w') as f2:
    f2.write(no_spaces)

