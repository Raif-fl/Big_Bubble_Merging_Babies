from typing import List, Dict, Iterable, Tuple
import copy

def is_source(node: str, G: Dict):
    edges = G[node]
    red = False
    blue = False
    for edge in edges:
        if edge[1] < 0:
            red = True
        elif edge[1] > 0:
            blue = True
    if red and blue:
        return True
    else:
        return False

def get_next_red_node(source, G):
    try:
        edges = G[source]
    except:
        return "nothing"
    candidate_nodes = []
    for edge in edges:
        if edge[1] > 0:
            candidate_nodes.append(edge[0])
    if len(candidate_nodes) == 0:
        return "nothing"
    elif source in candidate_nodes:
        next_node = copy.copy(source)
    else:
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
    try:
        edges = G[source]
    except:
        return "nothing"
    candidate_nodes = []
    for edge in edges:
        if edge[1] < 0:
            candidate_nodes.append(edge[0])
    ####this will have to change once we decide on how to resolve multiple edges
    if len(candidate_nodes) == 0:
        return "nothing"
    elif source in candidate_nodes:
        next_node = copy.copy(source)
    else:
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
    next_red_node = get_next_red_node(source, G)
    next_blue_node = get_next_blue_node(source,G)
    edit_count = 0
    node_l = k - 1
    change_tracker = ['' for i in range(node_l)]

    while True:

        if next_red_node == "nothing" or next_blue_node == "nothing":
            return edit_count

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
        if is_source(key, union):
            sources.append(key)
    ###!!!### Ok, So basically the keys of union are random which causes the error. 
    sources.sort()

    total_edits = 0
    #loop will continue while there are sources and eges in dict
    while len(sources) != 0 and len(union) > 0:
        current_source = sources[0]
        count = resolve_bubble(current_source, union, k)
        total_edits += count
        del sources[0]

    return total_edits