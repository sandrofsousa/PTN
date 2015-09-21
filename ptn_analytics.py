#################################################################################################################
##                                                                                                             ##
## ------------------------------ Public Transport Complex Network of São Paulo ------------------------------ ##
##                                                                                                             ##
## Empirical Analysis of GTFS data of São Paulo Public transport network (Bus, subway adn train systems)       ##
## from SPTrans. The bus stops and subway stations are set as vertex (nodes) and lines/routes as edges (links) ##
## of the network. Statistical analysis of the Network using graph theory,calculating degree distribution,     ##
## centrality, hubs, clusters and other network metrics.                                                       ##
##                                                                                                             ##
##  Sousa, Sandro                                                                                              ##
##  Complex Systems Modeling                                                                                   ##
##  University of São Paulo                                                                                    ##
##  sandrofsousa@gmail.com                                                                                     ##
##  sandrofs@usp.br                                                                                            ##
##                                                                                                             ##
#################################################################################################################


import networkx as nx
# import matplotlib.pyplot as plt

# TODO join metro networks to bus networks

# TODO
# Create directed Graph from edge list
source = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
el = open(source, 'rb')
PTN_D = nx.read_edgelist(el, delimiter=',', create_using=nx.DiGraph())
el.close()

# print(nx.attracting_components(PTN_D))
# print(nx.number_weakly_connected_components(PTN_D))
# print(nx.is_weakly_connected(PTN_D))
# print(list(nx.connected_components(PTN_D)))



# Create undirected Graph from edge list
# source = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
# el = open(source, 'rb')
# PTN_G = nx.read_edgelist(el, delimiter=',', create_using=nx.Graph())
# el.close()

# TODO plot degree distribution and info
print(nx.info(PTN_D))
# print(nx.degree_histogram(PTN_D))
# print(nx.info(PTN_G))
# print(nx.degree_histogram(PTN_G))
# print(nx.average_shortest_path_length(PTN_D))


# TODO plot metrics


# TODO draw graphs

# Validade lines