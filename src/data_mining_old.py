#!/usr/bin/python
#This module Extract sequence wise pallindrom out put from output file which contains more than one sequence
from sys import argv
import re
import os
#filename = '/Users/admin/Library/Mobile Documents/com~apple~CloudDocs/project/2ndscore_out/LCYG01000120.out'
#with open (filename, 'r') as f:
#    lines = f.read().splitlines()
def sndscore(fafile):
    os.system("transterm/2ndscore {} > {}".format(fafile, 'input/a.out'))

def seq_data(outfile = 'input/a.out'):
    with open (outfile, 'r') as f:
        lines = f.read().splitlines()
    seq_list = []
    d = {}
    for line in lines:
        if line[0] == '>':
            p = re.compile(r'\w+\.\d+/\d+\-\d+')
            seq_name = p.search(line).group()
            seq = []
            seq.append(seq_name)
            seq_list.append(seq)
            d[seq_name] = seq
        else:
            seq.append(line)
    return seq_list

def pall_data(outfile='input/a.out'):
    '''This function extract data from file in form of List of the word'''
    data_dict = {}
    #ldata = []                                 #list of the all lines in the file in form of word list'''
    for seq in seq_list:
        seq_name = seq[0]
        data = []
        data.append(seq_name)
        for line in seq[1:]:
            info = line.split()
            if info[0] != 'None':         #Eliminating bad data with no energy or pallindrome()
                data.append(info)
        #ldata.append(data)
        data_dict[seq_name] = data
    return data_dict

if __name__== "__main__":
    #seq_list = seq_data()
    #print(len(get_data()[0][-1]))
    #print(len(get_data()[1]['CP002825.1/2790786-2790690']))
    print()



'''def create_seq():
    seq = []
    return seq'''