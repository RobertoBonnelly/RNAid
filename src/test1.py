a,b=5,10
print(a)
#!/usr/bin env python
import pytest
import pdb
#rom src.fingerprint import path

graph = {0:[1,2,3,7,9],
        1:[7,4],
        2:[4,5,8],
        3:[8],
        4:[],
        5:[8],
        6:[],
        7:[],
        8:[],
        9:[]
      }

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
    
paths = path(graph,0)
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
    return paths
print(dag(paths))