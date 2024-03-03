from KF_functions import *
from typing import List, Dict, Iterable, Tuple


###larger kmers
#string_1 = 'GACTACTGAT'
#string_2 = 'GACAAAAGAT'

### Bubble:
string_1 = "ACGTACAT"
string_2 = "ACGTAGAT"


### Looper:
#string_1 = "AAAAA"
#string_2 = "AACAA"

### Split:
#string_1 = "ACGTACAT"
#string_2 = "ACGTACAG"

### Two snps right next to each other (big bubble).
#string_1 = "ACGTACAT"
#string_2 = "ACGGCCAT"

###!!!### Some weird looking stuff.
#string_1 = "ACGTACAT"
#string_2 = "ACGGAGAT"

#string_1 = "ACGTACATACA"
#string_2 = "ACGTAGATACA"

#string_1 = "ACGTAGATGCA"
#string_2 = "ACGCAGATACA"



repeat_1 = to_kmers(string_1, 4)
repeat_2 = to_kmers(string_2, 4)
db1 = de_bruijn_kmers(repeat_1)
db2 = de_bruijn_kmers(repeat_2)

union = union_graph(db1, db2)
print(union)

#balanced is defined as having at least 1 red and blue outgoing edges
def is_balanced(node: str, G: Dict):
    edges = G[node]
    #balanced = [0, 0]
    sum = 0
    for edge in edges:
        sum += abs(edge[1])
    #print(balanced)
    if sum%2 == 0:
        return True
    else:
        return False

def get_next_red_node(source, G):
    edges = G[source]
    candidate_nodes = []
    for edge in edges:
        if edge[1] > 0:
            candidate_nodes.append(edge[0])
    ####this will have to change once we decide on how to resolve multiple edges
    next_node = candidate_nodes[0]
    for i in range(0, len(edges)):
        edge = edges[i]
        node = edge[0]
        if edge[0] == next_node and edge[1] > 0:
            edge_count = edge[1] - 1
            del edges[i]
            if len(edges) == 0:
                del G[source]
            if edge_count != 0:
                edges.append((node, edge_count))
            break
    return next_node

def get_next_blue_node(source, G):
    edges = G[source]
    candidate_nodes = []
    for edge in edges:
        if edge[1] < 0:
            candidate_nodes.append(edge[0])
    ####this will have to change once we decide on how to resolve multiple edges
    next_node = candidate_nodes[0]
    for i in range(0, len(edges)):
        edge = edges[i]
        node = edge[0]
        if edge[0] == next_node and edge[1] < 0:
            edge_count = edge[1] + 1
            del edges[i]
            if len(edges) == 0:
                del G[source]
            if edge_count != 0:
                edges.append((node, edge_count))
            break
    return next_node



def resolve_bubble(source: str, G:Dict, k:int):
    '''
    iterate through source edges and assign 'starts' to red and blue branches. 
    will have to update to account for more than 2 outgoing (edge-picking)
    convention for this alg: red->positive, blue->negative
    '''
    print(source)
    print(G)
    next_red_node = get_next_red_node(source, G)
    #print(G)
    next_blue_node = get_next_blue_node(source,G)
    #print(G)
    edit_count = 0
    node_l = k - 1
    change_tracker = ['' for i in range(node_l)]

    while True:
        print('R: ' + next_red_node)
        print('B: ' + next_blue_node + '\n')

        for i in range(0, node_l):
            #python strings are immutable, have to make them lists
            red_str_list = list(next_red_node)
            blue_str_list = list(next_blue_node)

            #by convention red is the 'correct' string
            if change_tracker[i] != '':
                blue_str_list[i] = change_tracker[i]

            if blue_str_list[i] == red_str_list[i]:
                continue
            else:
                blue_str_list[i] = red_str_list[i]
                change_tracker[i] = red_str_list[i]
                edit_count += 1
        #shift the change tracker before moving to next nodes
        del change_tracker[0]
        change_tracker.append('')

        #stop if either blue or red doesnt have contiuation
        if next_blue_node not in G or next_red_node not in G:
            #print(change_tracker)
            return edit_count

        next_red_node = get_next_red_node(next_red_node, G)
        next_blue_node = get_next_blue_node(next_blue_node, G)

def transform_graph(union: Dict, k:int):
    sources = []
    for key in union:
        if is_balanced(key, union):
            sources.append(key)

    total_edits = 0
    #loop will continue while there are sources and eges in dict
    while len(sources) != 0 and len(union) > 0:
        current_source = sources[0]
        count = resolve_bubble(current_source, union, k)
        total_edits += count
        del sources[0]

    return total_edits

