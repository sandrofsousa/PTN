__author__ = 'sandrofsousa'

from igraph import *
from random import choice
from tqdm import tqdm
import numpy as np


def attack_node_targeted(file_input, rho, interactions):
    """
    Function to perform targeted attacks on network based on a node importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/node_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0         # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while True:                                                   # stop if counter reach interactions limit
            targeted_list = ptn.vs(_degree=ptn.maxdegree())['name']   # get node id with max degree
            for targeted_node in targeted_list:                       # loop at nodes if more than one has same degree
                data_out.write(str([
                    counter,
                    ptn.vcount(),
                    ptn.ecount(),
                    ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                    ptn.diameter(directed=True, unconn=True),
                    ptn.average_path_length(directed=True, unconn=True),
                    len(ptn.clusters(mode=WEAK)),
                    len(ptn.clusters(mode=STRONG)),
                    ptn.assortativity_degree(directed=True),
                    ptn.transitivity_undirected(),
                    ptn.density(),
                    targeted_node]) + "\n")
                ptn.delete_vertices(ptn.vs.find(name=targeted_node))  # delete node
                counter += 1                        # increase counter
            if counter >= interactions:
                break


def attack_node_random(file_input, rho, interactions):
    """
    Function to perform random attacks to nodes on network based on a random algorithm. Removes the target and
    calculate measures to find the impact of it. Receive a Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/node_random%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0         # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while True:
            all_nodes = ptn.vs()['name']             # get all nodes
            random_node = choice(all_nodes)          # return a random node from list
            data_out.write(str([
                counter,
                ptn.vcount(),
                ptn.ecount(),
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                # ptn.diameter(directed=True, unconn=True),
                # ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                random_node]) + "\n")
            ptn.delete_vertices(ptn.vs.find(name=random_node))  # delete node
            counter += 1                                        # increase counter
            if counter >= interactions:
                break


def attack_link_targeted(file_input, rho, interactions):
    """
    Function to perform targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/link_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            targeted_list = ptn.es(max(ptn.count_multiple()))   # get edge with max multiplicity
            for targeted_link in targeted_list:                 # loop at nodes if more than one has same degree
                data_out.write(str([
                    counter,
                    ptn.vcount(),
                    ptn.ecount(),
                    ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                    # ptn.diameter(directed=True, unconn=True),
                    # ptn.average_path_length(directed=True, unconn=True),
                    len(ptn.clusters(mode=WEAK)),
                    len(ptn.clusters(mode=STRONG)),
                    ptn.assortativity_degree(directed=True),
                    ptn.transitivity_undirected(),
                    ptn.density(),
                    targeted_link['trip']]) + "\n")
                ptn.delete_edges(targeted_link)  # delete node
                counter += 1                     # increase counter
            if counter >= interactions:
                break


def attack_link_random(file_input, rho, interactions):
    """
    Function to perform targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/link_random%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0
    with open(file_output, "w") as data_out:
        while counter <= interactions:                  # stop if counter reach interactions limit
            all_edges = ptn.es()                        # get all edges
            index_random = randrange(len(all_edges))    # get an index randomly from node list
            random_list = ptn.es[index_random]          # return edge id based on index
            for random_link in random_list:             # loop at nodes if more than one has same degree
                data_out.write(str([
                    counter,
                    ptn.vcount(),
                    ptn.ecount(),
                    ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                    ptn.diameter(directed=True, unconn=True),
                    ptn.average_path_length(directed=True, unconn=True),
                    len(ptn.clusters(mode=WEAK)),
                    len(ptn.clusters(mode=STRONG)),
                    ptn.assortativity_degree(directed=True),
                    ptn.transitivity_undirected(),
                    ptn.density(),
                    random_link['trip']]) + "\n")
                ptn.delete_edges(random_link)   # delete edge
                counter += 1                    # increase counter


def cut_articulation_points():
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/cuts.txt"
    radius = list(range(0, 200, 5))
    with open(file_output, "w") as result:
        for rho in radius:
            graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net%s.graphml" % rho
            ptn = Graph.Read_GraphML(graph)
            articulation_points = ptn.cut_vertices()
            result.write(str(articulation_points) + "\n")


def attack_scenarios():
    """
    Function to run all the attack scenarios for different values of rho processed before. It controls the networks
    to be analysed and the number of interactions the delete process will be removing items.
    """
    radius = [0, 20, 65, 150, 200]
    interactions = 100
    for rho in tqdm(radius):
        graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net%s.graphml" % rho
        # attack_node_targeted(graph, rho, interactions)
        # attack_node_random(graph, rho, interactions)
        attack_link_targeted(graph, rho, interactions)
        # attack_link_random(graph, rho, interactions)
        # cut_articulation_points()


# attack_scenarios()

rho = 0
graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net%s.graphml" % rho
# ptn = Graph.Read_GraphML(graph)
# print(ptn.edge_connectivity(checks=False))

# all_edges = ptn.es()
# index_random = randrange(len(all_edges))
# random_link = ptn.es[index_random]
# print(all_edges)
# print(index_random)
# print(random_link)

# targeted_link = ptn.es(max(ptn.count_multiple()))
# print(targeted_link()['trip'])
# print(targeted_link)

# max_es = ptn.es(_source=cc, _target=cc)
# print(max_es['trip'])
# <igraph.Graph object at 0x10fef25e8>, 85928, {'trip': '9501-10-1'})
# print(ptn.es()['trip'])

file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/link_target%s.txt" % rho
ptn = Graph.Read_GraphML(graph)
counter = 0
interactions = 20

targeted_list = ptn.es(max(ptn.count_multiple()))
test = ptn.es[0]
print(targeted_list)
print(test)


# with open(file_output, "w") as data_out:
#     while True:
#         targeted_list = ptn.es(max(ptn.count_multiple()))   # get edge with max multiplicity
#         for targeted_link in targeted_list:                 # loop at nodes if more than one has same degree
#             data_out.write(str([
#                 counter,
#                 ptn.vcount(),
#                 ptn.ecount(),
#                 ptn.maxdegree(vertices=None, mode=ALL, loops=True),
#                 # ptn.diameter(directed=True, unconn=True),
#                 # ptn.average_path_length(directed=True, unconn=True),
#                 len(ptn.clusters(mode=WEAK)),
#                 len(ptn.clusters(mode=STRONG)),
#                 ptn.assortativity_degree(directed=True),
#                 ptn.transitivity_undirected(),
#                 ptn.density(),
#                 targeted_link['trip']]) + "\n")
#             ptn.delete_edges(targeted_link)  # delete node
#             counter += 1                     # increase counter
#         if counter >= interactions:
#             break


# while True:
#     targeted_list = ptn.es(max(ptn.count_multiple()))   # get edge with max multiplicity
#     for targeted_link in targeted_list:                 # loop at nodes if more than one has same degree
#         print(
#             counter,
#             ptn.vcount(),
#             ptn.ecount(),
#             ptn.maxdegree(vertices=None, mode=ALL, loops=True),
#             # ptn.diameter(directed=True, unconn=True),
#             # ptn.average_path_length(directed=True, unconn=True),
#             len(ptn.clusters(mode=WEAK)),
#             len(ptn.clusters(mode=STRONG)),
#             ptn.assortativity_degree(directed=True),
#             ptn.transitivity_undirected(),
#             ptn.density(),
#             targeted_link['trip'])
#         ptn.delete_edges(targeted_link)  # delete node
#         counter += 1                     # increase counter
#     if counter >= interactions:
#         break
