#!/usr/bin/env python
'''Project: Towards the development of a simple fingerprint representation for
the efficient comparison and clustering of large datasets of RNA sequences
By: Abdulvahab Kharadi
First supervisor Name: Irilenia Nobeli
Date: 01/06/20
version: v2.0.0'''

# importing required module
from sys import argv
import cgi
#import cgitb
import hashlib
import re
import os
from data_mining import process_fa, get_data
#cgitb.enable()

def palindromes(data):
    '''This function take data from a file and return a list of palindromes.
    Each palindrome represented by a four cordinate, two for left steam and two for right steam'''
    palindrome= []
    for i in range(1,len(data)):
        word = data[i]
        energy = float(word[0])
        start = int(word[1])
        lsteam = re.sub('-','',word[5])           #Left steam of a pallindrome,cleaning data
        rsteam = re.sub('-','',word[7])           #Right steam of a pallindrome,cleaning data
        loop = word[6]
        length = int(word[3])
        p = [start,start+len(lsteam)-1,length-len(rsteam)+1,length]
        palindrome.append(p)
    return sorted(palindrome)                     # sorting list accrding to start position

def relation(p1,p2):
    '''This function take list of palindromes and return relationship between two palindromes in form of a Letter.
    Where O=overlapping,S=serial,X=exclusive,I=Included'''
    if p1[1] < p2[0] and p1[2] > p2[1] and p1[3] < p2[2]:
        return 'O'
    elif p1[1]<p2[0] and p1[2] > p2[3] :
        return 'I'
    elif p1[3] < p2[0]:
        return 'S'
    else:
        return 'X'

def pgraph(palindrome):
    '''This function give graph from each pallindrome (consider as Node) to another pallindrome.
    There is no path between pallindrome having Exclusive(X) relation.
    Rerurns dictionary which has Node as key and list of paths from that node as list'''
    #palindrome = palindromes()
    #print(len(palindrome))
    graph = {}
    for i in range(len(palindrome)):
        path = []
        for j in range(i,len(palindrome)):
            r = relation(palindrome[i],palindrome[j])
            if r != 'X':
                path.append(j)
                graph[i] = path
            else:
                graph[i] = path
    print(graph)
    return graph

def path(graph,start,p=[]):
    '''This function give complete paths from each pallindrome'''
    p = p + [start]
    if graph[start] == []:
        return [p]
    paths = []
    for node in graph[start]:
        if node not in p:
            new_paths = path(graph,node,p)
            for new_path in new_paths:
                paths.append(new_path)
    return paths


def dag(paths):
    for p in sorted(paths):
        for j in range(len(paths)-1):
            if set(p) < set(paths[j]):
                try:
                    paths.remove(p)
                    #da_graph = paths
                except:
                    next
                    continue
    return max(paths, key=len)

def fingerprint(da_graph,palindrome):
    '''This function provides a fingerprint for path from each node. We use hashlib to convert
    character presenting relation into a hash number'''
    paths_fingerprint = []
    i =0
    fp = ''
    while i<len(da_graph)-1:
        fp += relation(palindrome[i],palindrome[i+1])
        i += 1
    bfp = fp.encode('utf-8')                            #turn string into byte string
    hfp = hashlib.sha256(bfp)                           #turn bytes into hash object
    index= int(hfp.hexdigest(), 16) % 10**3
    paths_fingerprint.append(index)
    return paths_fingerprint

def tanimoto(s1, s2):
    s12 = set(s1).intersection(set(s2))
    tan = len(s12)/(len(s1) + len(s2) - len(s12))
    return tan

def accuracy(tan):
    if tan >= 0.8 :
        return tan80
    elif tan >= 0.6 and tan < 0.8:
        return tan60
    elif tan >= 0.4 and tan < 0.6:
        return tan40
    elif tan >= 0.2 and tan < 0.4:
        return tan20
    else:
        return tanbad

def run(filename=argv[1],result= {}):
    with open (filename,'r') as f:
        sequences = f.read().splitlines()
    i = 0
    while i < len(sequences):
        deal_single_seq(sequences,i)
        (seq_name, refine_data) = get_data()
        palindrome = palindromes(refine_data)
        graph = pgraph(palindrome)
        paths = path(graph,0)
        da_graph = dag(paths)
        paths_fingerprint = fingerprint(da_graph,palindrome)
        result[seq_name] = paths_fingerprint
        i += 2
    return result
def run_new(dir,result={}):
    for file in os.listdir(dir):
        temp_fa=f'{dir}/{file}'
        #process_fa(temp_fa)
        seq_name = get_data(temp_fa)[0]
        refine_data = get_data(temp_fa)[1]
        #(seq_name, refine_data) = get_data()
        print("1st and 2nd task completed: data_mining model")
        palindrome = palindromes(refine_data)
        print("palindrome function completed")
        graph = pgraph(palindrome)
        '''graph = {0:[1,2,3,7,9],
                1:[4,7],
                2:[4,5,8],
                3:[8],
                4:[],
                5:[8],
                6:[],
                7:[],
                8:[],
                9:[]}'''
        print("graph function completed")
        paths = path(graph,0)
        print("paths generated")
        da_graph = dag(paths)
        print("dag completed")
        paths_fingerprint = fingerprint(da_graph,palindrome)
        result[seq_name] = paths_fingerprint
        print("fingerprint generated")
    return result

if __name__ == '__main__':
    result = run_new(argv[1])
    print(result)

    done = []; tan80 = []; tan60 = []; tan40 = []; tan20 = []; tanbad = []
    accu = {'tan80':'0.8 to 1',
            'tan60' : '0.6 to 0.8',
            'tan40' : '0.4 to 0.6',
            'tan20' : '0.2 to 0.4',
            'tanbad' : '0 to 0.2' }

    for s1, fp1 in result.items():
        done.append(s1)
        for s2, fp2 in result.items():
            if s2 not in done:
                tan = tanimoto(fp1,fp2)
                group = accuracy(tan)
                group.append((s1, s2, tan))
    i = 0
    result_list = globals()[argv[2]]
    print('There are %d sequence pairs with tanimoto = %s' %(len(result_list),accu[argv[2]]))
    for result in result_list:
        i += 1
        print (result)
        print(f'{i}): Tanimoto for {result[0]} and {result[1]} is -> {result[2]}')
        if i % 10 == 0:
            input('Press Any Key to continue:\n')
