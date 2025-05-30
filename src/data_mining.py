#!/usr/bin/python
#This module Extract sequence wise pallindrom out put from output file which contains more than one sequence
from sys import argv
#import numpy as np
#import pandas as pd
import re
import os
import subprocess
import time

def second_score():
    #os.system("cd")
    rfam_id = 'RF00001'
    rfam_fol ='input/{}'.format(rfam_id)
    rfam_gz = '{}/{}.fa.gz'.format(rfam_fol, rfam_id)
    rfam_fa = '{}/{}.fa'.format(rfam_fol, rfam_id)
    rfam_out = '{}/{}.out'.format(rfam_fol, rfam_id)
    path = "ftp://ftp.ebi.ac.uk/pub/databases/Rfam/14.1/fasta_files/{}.fa.gz".format(rfam_id)
    os.system("wget -NP {} {}".format(rfam_fol, path))
    os.system("gzip -fd {}".format(rfam_gz))
    os.system("~/transterm/2ndscore {} > {}".format(rfam_fa, rfam_out))
    #os.popen("~/transterm/2ndscore Github/AK_Msc_Project/input/RF01084/RF01084.fa>")
    #subprocess.call("~/transterm/2ndscore Github/AK_Msc_Project/input/RF01084/RF01084.fa")

def pall_data(filename):
    data_dict = {}
    with open (filename, 'r') as f:
        lines = f.read().splitlines()
    for line in lines:
        if line[0] == '>':
            p = re.compile(r'\w+\.\d+/\d+\-\d+')
            seq_name = p.search(line).group()
        else:
            data = (line.split())
            if data[0] != 'None' and float(data[0]) < 0:
                refine_data.append(data)   
            data_dict[seq_name] = refine_data
    return data_dict

def deal_single_seq(sequences,i,temp_fa='input/temp.fa',temp_out = 'input/temp.out'):
    temp = sequences[i:i+2]
    seq = "\n".join(temp)
    print(seq)
    with open(temp_fa, 'w') as f:
        f.write(seq)
    os.system("transterm/2ndscore --no-rvs {} > {}".format(temp_fa, temp_out))
def process_fa(temp_fa, temp_out="temp.out"):
        os.system("transterm/2ndscore --no-rvs {} > {}".format(temp_fa, temp_out))
        #os.system("rm {}".format(temp_out))

def get_data(temp_out):

    ## empty list
    refine_data = []

    ## opening hairpins.out file obtained
    ## from 2ndscore
    with open (temp_out, 'r') as f:

        # splitting the file by sequence identifiers to separate multi-sequence
        # into multiple lists
        data_extractor = f.read().split(">")
        data_extractor.pop(0)
        obj = {}
        for i in data_extractor:
            lines = i.splitlines()
            
            seq_name = lines.pop(0)
            refine_data.append(seq_name)
            data = [line.split() for line in lines]
            obj[str(refine_data[data_extractor.index(i)])] = [d for d in data if d[0] != "None" and float(d[0]) <= 2]
            
            continue
        return [refine_data, obj]

def sndscore(dir="sequence"):
    starttime=time.time()
    i=0
    for file in os.listdir(dir):
        os.system("transterm/2ndscore {}/{}".format(dir,file))
        i+=1
    endtime=time.time()
    duration = (endtime - starttime) /60
    print(f'time taken to process{i} sequence is {duration} min')

if __name__== "__main__":
    print()
    #print(pall_data(argv[1]))
    #process_fa("sequence/g1_e.Characium_saccatum.C1SSU.fa")
    #seq_name, refine_data = get_data()
    #print(seq_name)
    #print(deal_single_seq("input/sample_RF01848.fa",0))
    #sndscore()
    dir="sequence"
    d1 = 0
    d2 = 0
    d = {}
    for file in os.listdir(dir):
        temp_fa=f'{dir}/{file}'
        start1 = time.time()
        process_fa(temp_fa)
        end1 = time.time()
        d1 += -start1+end1
        start2 = time.time()
        seq, data = get_data()
        d[seq] = data
        end2=time.time()
        d2 += -start2+end2
    print(d1, d2)
    print(len(d))
    for k,v in d.items():
        print(k, "---->", v)
