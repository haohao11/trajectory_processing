# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:40:16 2017
This is the module for CSV transpose
First: remove the hearder
seconde: transpose the row and the column

@author: cheng
"""

import csv
import os


def transpose(file):
    dirname = '..\data'
    if not os.path.exists(dirname):
        print("make the folder for the data")
        os.mkdir(dirname)
    filename = os.path.join(dirname, file)
    
    raw = zip(*csv.reader(open(filename, "r")))
    csv.writer(open(os.path.join(dirname, "transpose.csv"), "w", newline='')).writerows(raw)
    print("the transposed CSV is saved as transpose.csv")
    
    