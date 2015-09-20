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


# Function to read GTFS file from local directory and save processed result to a new file.
# Data time stamp = 04 Mar. 2015 at 17:47.

def gtfs_to_edge_list():
    rsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stop_times.txt"
    wsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edge_list.txt"
    with open(rsource, "r") as data, open(wsource, "w") as target:
        # create two equal lists containing file' lines
        file1 = file2 = [line.strip() for line in data]

        # loop reading the two lists created, where the second list is read from the second line.
        for line1, line2 in zip(file1, file2[1:]):

            # select the first column from line 1 and 2 (position 0).
            trip_old = line1.split(',')[0]
            trip_new = line2.split(',')[0]

            # select the fourth column from line 1 and 2 (position 3).
            stop_old = line1.split(',')[3]
            stop_new = line2.split(',')[3]

            # Compare if trip_id of line 1 is equal to trip_id of line 2.
            if trip_old == trip_new:

                # if true, write stop_id from line 1 and 2 to target file. Trip_id is preserved as edge label.
                target.writelines([stop_old + ',', stop_new + '\n'])
                continue
        # close files.
        data.close()
        target.close()

# gtfs_to_edge_list()


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
for g in nx.connected_component_subgraphs(PTN_D):
    print(nx.average_shortest_path_length(g))



# Create undirected Graph from edge list
# source = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
# el = open(source, 'rb')
# PTN_G = nx.read_edgelist(el, delimiter=',', create_using=nx.Graph())
# el.close()

# TODO plot degree distribution and info
# print(nx.info(PTN_D))
# print(nx.degree_histogram(PTN_D))
# print(nx.info(PTN_G))
# print(nx.degree_histogram(PTN_G))
# print(nx.average_shortest_path_length(PTN_D))


# TODO plot metrics


# TODO draw graphs
