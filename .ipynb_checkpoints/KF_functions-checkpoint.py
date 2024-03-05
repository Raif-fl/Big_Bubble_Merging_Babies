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
            brujin.update({pref: [suffixes[i]]})

    return (brujin)

def to_kmers(string, k):
    k_mers = {}
    for i in range(0, len(string) -k + 1):
        window = string[i:i+k]
        if window in k_mers.keys():
            k_mers[window] += 1
        else:
            k_mers[window] = 1
    return k_mers

def union_graph(db1, db2):
    union = {}
    for i in db1:
        try:
            y = union[i]
        except:
            union[i] = []
        try:
            x = db2[i]
            for j in db1[i]:
                if j not in x:
                    union[i].append((j))
        except:
            union[i] = []
            for j in db1[i]:
                union[i].append((j))

    for i in db2:
        try:
            y = union[i]
        except:
            union[i] = []
        try:
            x = db1[i]
            for j in db2[i]:
                if j not in x:
                    union[i].append((j[0], -1 * j[1]))
        except:
            union[i] = []
            for j in db2[i]:
                union[i].append((j[0], -1 * j[1]))

    # Remove nodes that go nowhere from the Trie:
    union = {key: value for key, value in union.items() if value}
    return union
