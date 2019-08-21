import networkx as nx
import csv
import seaborn as sns
import time
import numpy as np
from networkx.algorithms import bipartite

path_data = './dataset/User_Item_BIPARTITE_GRAPH___UserID__ItemID.tsv'
ground_truth_path = './dataset/Ground_Truth___UserID__ItemID.tsv'

def load_grapgh(path):
    myGraph = nx.Graph()
    myGraph = nx.read_edgelist(path, nodetype = int)
    print('Graph loaded correctly!')
    return myGraph

def get_graph_info(graph):
    print('Is the graph bipartite? ==> ' + str(nx.is_bipartite(graph)))
    print(nx.info(graph))


def get_projected_graph(graph, items):
    G = bipartite.generic_weighted_projected_graph(graph, set(items))
    return G

def get_items_to_project(path):
    l = []
    with open(path_data) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        for row in reader:
            l.append(int(row[1]))
    return l

def get_pagerank(bipartite, projected):
    users = list(set(bipartite).difference(set(get_items_to_project(path_data))))
    pageranks = {}

    for i in users:
        personal = {j:1 for j in bipartite.neighbors(i)}
        pagerank = nx.pagerank_numpy(projected, alpha=0.1, personalization=personal)
        pageranks[i] = pagerank

    for key, dic in pageranks.items():
        #deleting items already "known" by user
        items_not_in_B = set(dic).difference(set(bipartite.neighbors(key)))
        restricted_dic = {i:dic[i] for i in items_not_in_B}
        #sorting the dictionary
        pageranks[key] = dict(sorted(restricted_dic.items(), key=lambda kv: kv[1], reverse=True))
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
    print('Grabbing items to project...')

    items_to_project = get_items_to_project(path_data)
    print('Finished grabbing items!')
    print('\n')
    print('\n')
    print('Projected-item-item-graph... ')
    print('\n')
    G = get_projected_graph(B, items_to_project)
    print('\n')
    print('Projected graph initiated successfully!')
    print('\n')
    print('Projected graph info: ')
    get_graph_info(G)
    print('\n')
    print('########################')
    print('\n')

    print('Computing a Topic-Specific pagerank over the projected graph...')
    pagerank = get_pagerank(B, G)
    print('Ranking complete!')
    print('\n')
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
    r_precision_values = get_r_precision(pagerank, GT)
    avg_r_precision = get_average_r_precision(r_precision_values)
    print('\n')
    print('The average R-Precision value is: ', avg_r_precision)

    print('\n')
    print('########################')
    print('\n')

    print('Plotting the R-Precision distribution...')

    sns.set(color_codes=True)
    plt.figure(figsize=(12, 8))
    ax = sns.distplot(r_precs)
    ax.set(xlabel='R-precision', ylabel='Relative frequency')
    ax.show()

    end = time.time()
    elapsed = end-start

    print('The total time of execution for part 2.1 has been: ', elapsed)

if __name__ == '__main__':
    main()


