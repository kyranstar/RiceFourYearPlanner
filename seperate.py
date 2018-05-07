# -*- coding: utf-8 -*-
"""
Created on Sun May  6 20:16:04 2018

@author: Kyran Adams
"""

import collections

# Script to seperate a full class listing into listings for each subject

file = "FullClassList2018.txt"
with open(file, "r") as fin:
    classes = fin.readlines()

all_classes = collections.defaultdict(lambda: [])
for class_name in classes:
    all_classes[class_name[:4]].append(class_name)
    
for subject, class_names in all_classes.items():
    filename = "%sList2018.txt" % subject
    with open(filename, "w") as fout:
        for class_name in class_names:
            fout.write(class_name)
        