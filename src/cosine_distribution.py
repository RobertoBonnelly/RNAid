import os
import re
import networkx as nx
from itertools import product
from collections import Counter
def get_data(hairpins_file, max_energy):

    ## empty list
    refine_data = []

    ## opening hairpins.out file obtained
    ## from 2ndscore
    with open (hairpins_file, 'r') as f:

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
            obj[str(refine_data[data_extractor.index(i)])] = [d for d in data if d[0] != "None" and float(d[0]) <= max_energy]
            
            continue
        return [refine_data, obj]
    
def palindromes(data):
    '''This function (called new_palindromes in Roberto's notebook) takes the refined data 
    from a get_data and returns a dictionary with sequences as keys 
    and a list of palindromes as the value for each key.
    Each palindrome represented by a four cordinate, two for left steam and two for right steam'''
    ## creates empty dictionary   
    palindrome= {}
    ## itirates through the refined data
    for seqname in data: # each seqname is a sequence header (the key in the dictionary)
        # create empty list that will contain the palindromes
        pal_list = []
        ## word divides each line in a list
        for j in data[seqname]:
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
        palindrome[seqname]=sorted(pal_list)
    return palindrome                 # sorting list accrding to start position

def relation(p1,p2):
    '''This function take list of palindromes and return relationship between two palindromes in form of a Letter.
    Where O=overlapping,S=serial,X=exclusive,I=Included'''
    if p1[3] < p2[0]:
        return 'S'
    elif p1[1] < p2[0] and p1[2] > p2[1] and p1[3] < p2[2]:
        return 'O'
    elif p1[1]<p2[0] and p1[2] > p2[3] :
        return 'I'
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
        for j in range(i+1,len(palindrome)):
            r = relation(palindrome[i],palindrome[j])
            if r != 'X':
                path.append(j)
        graph[i] = path #moving this here ensures the last i will also have an empty path added
    return graph

def build_directed_graph_from_dict(graph_dict):
    """
    Builds a directed NetworkX graph from a dictionary where keys are vertex names
    and values are lists of connected vertices. The direction of edges is determined
    by alphanumeric comparison of the vertex names (smaller -> larger).

    Parameters:
    graph_dict (dict): A dictionary representing the graph adjacency list.

    Returns:
    networkx.DiGraph: The constructed directed graph.
    """
    G = nx.DiGraph()

    for node, neighbors in graph_dict.items():
        G.add_node(node)
        for neighbor in neighbors:
            # Determine direction based on alphanumeric order
            if node < neighbor:
                G.add_edge(node, neighbor)
            else:
                G.add_edge(neighbor, node)

    return G

def find_paths_up_to_length(G, l):
    """Finds all paths from each node up to length l, sorted by path length."""
    all_paths = {}
    for node in G.nodes():
        stack = [(node, [node])]  # (current_node, current_path)
        node_paths = []
        while stack:
            current_node, current_path = stack.pop()
            # Add path if it's within the length limit
            if len(current_path) <= l:
                node_paths.append(current_path.copy())
                # Explore neighbors if we haven't reached length limit
                if len(current_path) < l:
                    for neighbor in G.successors(current_node):
                        if neighbor not in current_path:  # Avoid cycles
                            stack.append((neighbor, current_path + [neighbor]))
        # Sort paths first by length, then lexicographically
        node_paths.sort(key=lambda x: (len(x), x))
        all_paths[node] = node_paths
    return all_paths

def fingerprint(graph, palindromes, max_path_length):
    '''This function creates a fingerprint by concatenating the relationships between palindromes along a path in a directed graph'''
    uniq_rel = []
    rel_list=[]
    fp = ''
    
    #find all the paths up to a certain length starting from each node in the graph
    all_paths = find_paths_up_to_length(graph, 5)

    #go through every node and path and create a set of unique character strings describing 
    #the relationships between all nodes (palindromes)
    for node, paths in all_paths.items():
        rel=''  #every node has a string built from all the relationships encountered in the paths
        for path in paths:
            if (len(path)>1):
                for i in range(len(path)-1):
                    rel += relation(palindromes[path[i]], palindromes[path[i+1]])   
                rel += ';' #separate paths
        if (rel == ''): #nothing has been added
            rel = '-' #to indicate that this node is on its own and has no paths to others
        rel_list.append(rel)
    return(rel_list)

def extract_first_elements(list_of_lists):
    """Extracts the first element from each sublist in a list of lists."""
    scores = []
    for sublist in list_of_lists:
        #score = list_of_lists[sublist]
        for i in list_of_lists[sublist]:
            #print("i=", i)
            score = float(i[0])
            scores.append(score)
    return scores

# extracting length of each hairpin
def extract_length(list_of_lists):
    """Extracts the length of each hairpin from a list of lists."""
    lengths = []
    for sublist in list_of_lists:
        #score = list_of_lists[sublist]
        for i in list_of_lists[sublist]:
            #print("i=", i)
            length = int(i[3])-int(i[1])
            lengths.append(length)
    return lengths

def custom_encoding_table():
    """This function uses the relationships Inclusive, Overlapping and
    Serial from the paths generated from the fingerprint function to create
    a table similar to ascii, but utilizing all possible combinations of these 3
    relations on strings up to 5 characters (363 combinations) and giving a custom
    value to each combination"""
    # chars representing Inclusive, Overlapping and Serial relations
    chars = ['I', 'O', 'S']
    # define table as a dictionary with combination as key and bit index as value
    table = {}
    # define index starting point
    index = 0
    for length in range(1, 6):
        for comb in product(chars, repeat=length):
            table[''.join(comb)] = index
            index += 1
    return table

## pre-create table
custom_feature_table = custom_encoding_table()
custom_feature_table["-"] = 363
energy_bins = [(-10.0, -7.0), (-7.0, -5.0), (-5.0, -3.0), (-3.0, -1.0), (-1.0, 1.5),
               (1.5, 2.5), (2.5, 3.5), (3.5, 4.5), (4.5, 5.5), (5.5, 6.5), (6.5, 7.5), (7.5, 9.0)]
length_bins = [(10), (11), (12), (13), (14), (15), (16), (17), (18), (19), (20, 25), (26, 30), (31, 35), 
               (36, 40), (41, 45), (46, 60)]

## function for new counts_vector builder
def counts_vector(features: list[str], lengths: list[int], energies: list[float]) -> list[int]:
    # deterministic size of vector
    size = len(length_bins) + len(energy_bins) + len(custom_feature_table)
    # create vector of 0's
    bit_vector = [0] * size

    # encode lengths
    for length in lengths:
        for i, bin in enumerate(length_bins):
            if type(bin) is int:
                if bin==length:
                    bit_vector[i] += 1
                    break
            elif type(bin) is tuple:
                if bin[0]<=length<=bin[1]:
                # add +1 to corresponding index
                    bit_vector[i] += 1
                    break  # only one bin should match

    # encode energies
    for energy in energies:
        for i, (low, high) in enumerate(energy_bins):
            if low <= energy <= high:
                bit_vector[len(length_bins) + i] += 1
                break

    # encode features (token counts)
    # set starting index for features
    offset = len(length_bins) + len(energy_bins)
    # set counter
    counter = Counter()
    # iterate over features
    for path in features:
        # iterate over paths in features
        tokens = [t.strip() for t in path.split(';') if t.strip()]
        for token in tokens:
            # determine token's index and add to the count
            if token in custom_feature_table:
                counter[token] += 1
    # iterate over counts to add each combination's count to the vector
    for token, count in counter.items():
        idx = custom_feature_table[token]
        bit_vector[offset + idx] = count

    return bit_vector

dataset = os.listdir('../RFAM')

rfam_vectors = []

for file in dataset:
    if file.endswith('.out'):
        (seq_name, hairpins) = get_data(os.path.join('../RFAM', file), 10)
        rfam_pals = palindromes(hairpins)
        rfam_lengths = extract_length(hairpins)
        rfam_energies = extract_first_elements(hairpins)
        for seq in rfam_pals:
            rfam_graph = pgraph(rfam_pals[seq])
            G = build_directed_graph_from_dict(rfam_graph)
            rfam_fp = fingerprint(G, rfam_pals[seq], 5)
            rfam_counts = counts_vector(rfam_fp, lengths=rfam_lengths, energies=rfam_energies)
            rfam_vectors.append(rfam_counts)
print("The length of the final vectors list is:", len(rfam_vectors))