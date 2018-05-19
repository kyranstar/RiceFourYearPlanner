# -*- coding: utf-8 -*-
"""
Created on Fri May 18 23:06:58 2018

@author: Kyran Adams
"""

import numpy as np
import os
import pandas as pd
import run_whole_dir
import pathlib

class PlanModel:
    
    def __init__(self, max_classes_per_sem=8, years=4):
        
        self.plan = pd.DataFrame(index=range(max_classes_per_sem),
                                 columns=pd.MultiIndex.from_product([
                                         range(years), 
                                         ["fall", "spring", "summer"]]))
        
    def set_class(self, class_name, year, semester, row):
        self.plan[year, semester][row] = self.__class_from_name(class_name)
        
    def get_class(self, year, semester, row):
        return self.plan[year, semester][row]
    
    def save(self, save_file):
        self.plan.to_csv(save_file, sep='\t')
        
    def open_file(self, save_file):
        self.plan = pd.read_table(save_file)        
    def __class_from_name(self, name):
        """
        Gives a (department, number) given a classname string.
        """
        name = name.strip()
        parts = name.split(' ')
        num_words = len(parts)
        if num_words != 2 or len(parts[0]) != 4 or len(parts[1]) != 3:
            return None
        else:
            parts[0] = parts[0].upper()
            return tuple(parts)

class ClassData:
    
    def __init__(self):
        self.read_data()
    
    def update_data(self):
        run_whole_dir.main()
        self.read_data()
    
    
    def read_data(self):
        offerings = filter(lambda filename: filename.endswith("Offerings.txt"),os.listdir("data"))
        self.class_data = {}
        for subject_offering in offerings:
            subject_code = subject_offering[:4]
            df = pd.read_table("data/" + subject_offering)
            df.set_index('Class name', inplace=True)
            self.class_data[subject_code] = df
    
    def class_exists(self, class_pair):
        class_name = "%s %s" % class_pair
        df = self.class_data[class_pair[0]]
        return class_name in df.index
    
    def offered_last_semester(self, class_pair, semester):
        class_name = "%s %s" % class_pair
        df = self.class_data[class_pair[0]]
        
        last_sem_col = "%s:%s" % ((df.columns[-1])[:4], semester)
        if not last_sem_col in df.columns:
            last_sem_col = "%s:%s" % ((df.columns[-2])[:4], semester)
        return df[last_sem_col][class_name] == 1.0
    
    def num_last_semesters_offered(self, class_pair, semester):
        pass
    
    #def distribution(self, class_pair, year, semester):
    #
    #def credit_hours(self, class_pair, year, semester):
    #    pass