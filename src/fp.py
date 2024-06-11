#!/usr/bin/env python
'''Project: Towards the development of a simple fingerprint representation for
the efficient comparison and clustering of large datasets of RNA sequences
By: Abdulvahab Kharadi
First supervisor Name: Irilenia Nobeli
Date: 08/08/2019
version: v3.0.0'''

# importing required module
from sys import argv
#import cgi
#import cgitb
import hashlib
import re
import os
from data_mining import process_fa, get_data
#cgitb.enable()
class Stem(object):
    pallindrome = []
    def __init__(self, data):
        '''This will instantiate a stem object with attributes such as right stem coordinates, left steam coordinates, free energy etc.''' 
        self.stem = data
        self.energy = float(self.stem[0])
        self.start = int(self.stem[1])
        self.lsteam = re.sub('-','',self.stem[5])           #Left steam of a pallindrome,cleaning data
        self.rsteam = re.sub('-','',self.stem[7])           #Right steam of a pallindrome,cleaning data
        self.loop = self.stem[6]
        self.length = int(self.stem[3])
        self.lstart = self.start
        self.lend = self.start+len(self.lsteam)-1
        self.rstart = self.length-len(self.rsteam)+1
        self.rend = self.length
    def __repr__(self):
        return f"The object is {self.rstart}"
                              
def run(dir,result={}):
    for file in os.listdir(dir):
        temp_fa=f'{dir}/{file}'
        process_fa(temp_fa)
        if get_data():
            (seq_name, refine_data) = get_data()
        print("1st and 2nd task completed: data_mining model")
        seq_info = {}
        for i in range(0,len(refine_data)):   
            seq_info[i] = Stem(refine_data[i])
            result[seq_name] = seq_info
    return result
if __name__=='__main__':
    result = run(argv[1])
    i = 0
    for k,v in result.items():
        while i < 2: 
            print (v[1])
            i += 1