import gzip
import os
#makes sure non-function code is commented out for these imports to work
from KF_functions2 import *
from alg_main_HSE2 import *
import copy

find_it = "/Users/keeganflanagan/Desktop/UCSD_Year_1/HELL/Big_Bubble_Merging_Babies"

gz_file = find_it + '/data/genome_2/genome/test-genome_2.fna.gz'
gz_mutate01 = find_it + '/data/genome_2/mut_genome_2/0.01/test-genome_2.fna.gz'
gz_mutate05 = find_it + '/data/genome_2/mut_genome_2/0.05/test-genome_2.fna.gz'
gz_mutate1 = find_it + '/data/genome_2/mut_genome_2/0.1/test-genome_2.fna.gz'
gz_mutate15 = find_it + '/data/genome_2/mut_genome_2/0.15/test-genome_2.fna.gz'

altered = [gz_mutate01, gz_mutate05, gz_mutate1, gz_mutate15]

def load_genome(gz_file):
    with gzip.open(gz_file, 'rb') as input:
        for line in input:
            l = line.strip().decode('utf-8')
            if l[0] == '>':
                continue
            else:
                genome = l
    return genome

def true_stats(g1, g2, k):
    positions = []
    for i in range(0, len(g1)):
        if g1[i] != g2[i]:
            positions.append(i)
    print(str(len(positions)) + ' changes at ' + str(positions))

def run_transform(g1, g2, k):
    repeat_1 = to_kmers(g1, k)
    repeat_2 = to_kmers(g2, k)
    db1 = de_bruijn_kmers(repeat_1)
    db2 = de_bruijn_kmers(repeat_2)

    union, purple = union_graph(db1, db2)
    #union = incomplete_edge_adjustment(union, purple)
    print(transform_graph(union, k))
    return

original = load_genome(gz_file)
mutated = []
for file in altered:
    mutated.append(load_genome(file))

for m in mutated:
    true_stats(original, m, 10)
    run_transform(original, m, 10)