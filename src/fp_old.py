#!/usr/bin/env python
'''Project: Towards the development of a simple fingerprint representation for
the efficient comparison and clustering of large datasets of RNA sequences
By: Abdulvahab Khardi
First supervisor Name: Irilenia Nobeli
Date: 22/05/2018,12/07/2018,15/08/2018
version: v1.0, v1.2.0, v1.2.1'''
# importing required module
from sys import argv
import hashlib
import re
import os
from data_mining import process_fa,get_data
#from data_mining_old import seq_data, pall_data
#seq = list_seq()[1][2]
# Enter palindrome file name  in cmd , we using 2ndscore to generate one from RNA sequences
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
        if energy < 0:
            p = (start,start+len(lsteam)-1,length-len(rsteam)+1,length)
            palindrome.append(p)
    #print(sorted(palindrome))
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
    #print(graph)
    return graph

def path(graph,start,p=[]):
    '''This function give complete paths from each pallindrome'''
    p = p + [start]
    if graph[start] == []:
        return [p]
    #if not (start in pgraph):
        #return [p]
    paths = []
    for node in graph[start]:
        if node not in p:
            new_paths = path(graph,node,p)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

def all_paths(palindrome,graph):
    allpaths = {}
    for i in range(0,len(palindrome)):
        allpaths[i] = path(graph,i)
    return allpaths

def fingerprint(palindrome, allpaths):
    '''This function provides a fingerprint for path from each node. We use hashlib to convert
    character presenting relation into a hash number'''
    d_fingerprint = {}
    paths_fingerprint = []
    for node,paths in allpaths.items():
        for path in paths:
            fp = ''
            for i in range(len(path)-1):
                fp += relation(palindrome[path[i]],palindrome[path[i+1]])
                bfp = fp.encode('utf-8')    #turn string into byte string
                hfp = hashlib.sha256(bfp)   #turn bytes into hash object
                index= int(hfp.hexdigest(), 16) % 10**3
                #print(index)
                paths_fingerprint.append(index)
        d_fingerprint[node] = paths_fingerprint
    return paths_fingerprint

def tanimoto(s1, s2):
    s12 = s1.intersection(s2)
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
def run_new(dir,result={}):
    for file in os.listdir(dir):
        temp_fa=f'{dir}/{file}'
        process_fa(temp_fa)
        (seq_name, refine_data) = get_data()
        print("1st and 2nd task completed: data_mining model")
        palindrome = palindromes(refine_data)
        print("palindrome function completed")
        graph = pgraph(palindrome)
        allpaths = all_paths(palindrome,graph)
        fp = fingerprint(palindrome, allpaths)
        #all_fingerprint[seq_name] = set(fp)
        #print("graph function completed")
        #paths = path(graph,0)
        #print("paths generated")
        #da_graph = dag(paths)
        #print("dag completed")
        #paths_fingerprint = fingerprint(da_graph,palindrome)
        result[seq_name] = set(fp)
        print("fingerprint generated")
    return result


if '__name__ ==__main__':
    #all_fingerprint = {}
    #seq_list = seq_data(fafile)      
    #for seq_name, data in pall_data(fafile).items():
    #    palindrome = palindromes(data)
    #    graph = pgraph()
    #    allpaths = all_paths()
    #    fp = fingerprint()
    #    all_fingerprint[seq_name] = set(fp)
    #print(all_fingerprint)
    result = run_new(argv[1])
    done = []; tan80 = []; tan60 = []; tan40 = []; tan20 = []; tanbad = []
    accu = {'tan80':'0.8 to 1',
            'tan60' : '0.6 to 0.8',
            'tan40' : '0.4 to 0.6',
            'tan20' : '0.2 to 0.4',
            'tanbad' : '0 to 0.2' }
    for s1, fp1 in result.items():
        done.append(s1)
        for s2, fp2 in all_fingerprint.items():
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