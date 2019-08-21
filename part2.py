import networkx as nx
import csv
import time
import matplotlib.pyplot as plt
import pandas as pd
from functools import reduce
from ast import literal_eval

path_data = './dataset/Base_Set___UserID__ItemID__PART_2_2.tsv'
path_pagerank = "./dataset/ItemID__PersonalizedPageRank_Vector.tsv"

def load_grapgh(path):
    myGraph = nx.Graph()
    myGraph = nx.read_edgelist(path, nodetype = int)
    print('Graph loaded correctly!')

    return myGraph

def get_graph_info(graph):
    print('Is the graph bipartite? ==> ' + str(nx.is_bipartite(graph)))
    print(nx.info(graph))

def get_items(path):
    l = []
    with open(path_data) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            item_x = row[1]
            l.append(int(item_x))
    return l

def get_pagerank(bipartite):
    pageranks={}
    df = pd.read_csv(path_pagerank, sep="\t", header=None,
        converters={1: literal_eval}, index_col=0, names=["pagerank"])
    #from list of couples to dictionary
    df["pagerank"] = df.apply(func=lambda x:  dict(x["pagerank"]), axis=1) 

    for i in users:
        n = list(bipartite.neighbors(i)) #list of neighbors of user i
        neigh_pageranks = list(df.loc[n]["pagerank"]) #set of pageranks only its neighbors
        #pageranks[i] = dict([(k,sum([df.loc[j]["pagerank"][k] for j in n])) for k in items2])
        pageranks[i] = reduce(lambda x, y: dict((k, v + y[k]) for k, v in x.items()), neigh_pageranks)
    
    return pageranks


def get_r_precision_distribution(pagerank, groundTruthGraph):
    r_precs = []
    for key,dic in pagerank.items():
        if key in groundTruthGraph.nodes():
            gt = set(groundTruthGraph.neighbors(key))
            r = len(gt)
            items = set(list(dic)[:r])
            inters = items.intersection(gt)
            r_precs.append(len(inters)/r)
    return r_precs

def get_average_r_precision(distr):
    mean_r_prec = sum(distr)/len(distr)
    return mean_r_prec

def main():
    start = time.time()
    print('Loading bipartite graph...')
    B = load_grapgh(path_data)
    print('\n')
    print('Bipartite graph info: ')
    get_graph_info(B)
    print('\n')
    print('########################')
    print('\n')
    
    items= set(get_items(path_data))
    users = set(B).difference(items)
    print("We have %s items and %s users"%(len(items),len(users)))

    print('\n')
    print('########################')
    print('\n')

    print('Obtaining pagerank...')
    pgrnk = get_pagerank(B)

    print('\n')
    print('########################')
    print('\n')

    print('Loading ground-truth graph...')
    GT = load_grapgh(ground_truth_path)
    print('\n')
    print('Ground-truth graph info: ')
    get_graph_info(GT)
    print('\n')
    print('########################')
    print('\n')

    print('Computing the Average-R-precision value...')
    r_precision_values = get_r_precision(pgrnk, GT)
    avg_r_precision = get_average_r_precision(r_precision_values)
    print('\n')
    print('The average R-Precision value is: ', avg_r_precision)

    end = time.time()
    elapsed = end-start

    print('The total time of execution for part 2.2 has been: ', elapsed)

if __name__ == '__main__':
    main()