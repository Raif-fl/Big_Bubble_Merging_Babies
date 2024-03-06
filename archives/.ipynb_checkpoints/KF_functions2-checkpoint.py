from typing import List, Dict, Iterable, Tuple
import copy

def suffix(string):
    return string[1:]
def prefix(string):
    return string[0:len(string)-1]

def de_bruijn_kmers(k_mers):
    # Get the prefixes and suffixes. 
    prefixes = []
    suffixes = []
    for i in k_mers:
        prefixes.append(prefix(i))
        suffixes.append((suffix(i), k_mers[i]))
    
    # Build up the Debrujin
    brujin = {}
    for i, pref in enumerate(prefixes):
        if pref in list(brujin.keys()):
            brujin[pref].append(suffixes[i])
        else:
            brujin.update({pref:[suffixes[i]]})

    return(brujin)

def to_kmers(string, k):
    k_mers = {}
    for i in range(0, len(string) -k + 1):
        window = string[i:i+k]
        if window in k_mers.keys():
            k_mers[window] += 1
        else:
            k_mers[window] = 1
    return k_mers

def union_graph(db1,db2):
    union = {}
    purple = {}
    all_keys = set(list(db1.keys()) + list(db2.keys()))
    for key in all_keys:
        # Makes sure the key is already in union. 
        try:
            blank = union[key]
        except:
            union[key] = []
            purple[key] = []
    
        # Checks to see if this key is present in the first De-bruijn, and if not 
        # adds the information at that key to the union graph
        try:
            x = db1[key]
        except:
            for j in db2[key]:
                union[key].append((j[0],-1*j[1]))
            continue
    
        # Checks to see if this key is present in the second De-bruijn, and if not 
        # adds the information at that key to the union graph
        try:
            y = db2[key]
        except:
            for i in db1[key]:
                union[key].append((i))
            continue
    
        ###!!!### This is definitely a bit slow, but it is the only way to ensure that it works perfectly right now. 
        for i in db1[key]:
            if i[0] not in [z[0] for z in db2[key]]:
                union[key].append((i[0],i[1]))
            if i in db2[key]:
                purple[key].append(i[0])
                
        for j in db2[key]:
            if j[0] not in [z[0] for z in db1[key]]:
                union[key].append((j[0],-1*j[1]))
        
        for i in db1[key]:
            for j in db2[key]:
                if i[0] == j[0]:
                    if i[1] != j[1]:
                        union[key].append((i[0], i[1] - j[1]))
                        
        if len(purple[key]) == 0:
            del purple[key]
        if len(union[key]) == 0:
            del union[key]
    return (union,purple)

def reverse_union_graph(union):
    reverse_union = {}
    for i in union:
        for j in union[i]:
            try:
                reverse_union[j[0]].append((i,j[1]))
            except:
                reverse_union[j[0]] = [(i,j[1])]
    return reverse_union

def wallbreak(infront, wall, behind, G, sign):
    try:
        G[infront].remove((wall, sign))
    except:
        blank = "nothing"
    try:
        G[behind].append((wall, sign))
    except:
        G[behind] = []
        G[behind].append((wall, sign))

def incomplete_edge_adjustment(union, purple):
    reverse_union = reverse_union_graph(union)
    for i, j in purple.items():
        for k in j:
            try:
                blank = union[k]
            except:
                continue
            if len(union[k]) == 1:
                try:
                    infront, sign = reverse_union[k][0]
                    wallbreak(infront, k, i, union, sign)
                    reverse_union[k].remove(infront, sign)
                except:
                    continue
                            
    union= {key:value for key,value in union.items() if value}
    return union