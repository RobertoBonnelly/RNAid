import os
import re
def get_data(temp_out):

    if os.path.exists(temp_out):
        
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
                obj[str(refine_data[data_extractor.index(i)])] = [d for d in data if d[0] != "None" and float(d[0]) <= 0]
                
                continue
            return obj
    else:
        raise FileExistsError(f"The file {temp_out} does not exist.")
    
def new_palindromes(data):
    '''This function takes the refined data from a get_data and returns a list of palindromes.
    Each palindrome represented by a four cordinate, two for left steam and two for right steam'''
    ## creates empty list   
    palindrome= {}
    ## itirates through the refined data
    for i in data: # each i is a sequence header (the key in the dictionary)
        # create empty list that will contain the palindromes
        pal_list = []
        ## word divides each line in a list
        for j in data[i]:
            word = j

            energy = float(word[0])

            ## start is the base where hairpin starts
            start = int(word[1])

            ## positions 5 and 7 tend to have - character
            ## here we remove them left being 5, and right 7
            lsteam = re.sub('-','',word[5])           #Left steam of a pallindrome,cleaning data
            rsteam = re.sub('-','',word[7])           #Right steam of a pallindrome,cleaning data

            loop = word[6]

            ## index 3 represents the lenght of the hairpin
            length = int(word[3])

            p = [start,start+len(lsteam)-1,length-len(rsteam)+1,length]
            pal_list.append(p)        
        palindrome[i]=sorted(pal_list)
    return palindrome                 # sorting list accrding to start position

def new_pgraph(palindrome):
    '''This function give graph from each palindrome (consider as Node) to another palindrome.
    There is no path between palindrome having Exclusive(X) relation.
    Rerurns dictionary which has Node as key and list of paths from that node as list'''
    xgraph = {}
    for i in palindrome:
        graph = {}
        ## itirates through each element in the palindromes list
        ## note that palindromes is a list of lists
        for j in range(len(palindrome[i])):
            ## empty list for each list in palindrome
            path = []
            ## itirates through palindome iteration
            for p in range(j,len(palindrome[i])):
                r = relation(palindrome[i][j],palindrome[i][p])
                if r != 'X':
                    path.append(p)
                    graph[j] = path
                else:
                    graph[j] = path
        xgraph[i] = graph
    return xgraph

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

def new_pathsfunc(graph,start,p=[]):
    '''This function give complete paths from each pallindrome'''
    dpaths = {}
    for i in graph:
        p = p + [start]
        if graph[i][start] == []:
            return [p]
        paths = []
        for node in graph[i][start]:
            if node not in p:
                new_paths = path(graph[i],node,p)
                for new_path in new_paths:
                    paths.append(new_path)
        dpaths[i] = paths
        p.clear()
    return dpaths

def new_dag(paths):
    dags = {}
    for i in paths:
        for p in sorted(paths[i]):
            for j in range(len(paths[i])-1):
                if set(p) < set(paths[i][j]):
                    try:
                        paths.remove(p)
                        #da_graph = paths
                    except:
                        next
                        continue
        dags[i]=max(paths[i], key=len)
    return dags

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