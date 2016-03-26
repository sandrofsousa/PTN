__author__ = 'sandrofsousa'

from igraph import *
from random import randrange


def attack_node_targeted(file_input, rho):
    """ Function to perform targeted attacks on network based on a node importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/target_node%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    interactions = 3
    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            targeted_node = ptn.vs(_degree=ptn.maxdegree())  # get node id with max degree
            data_out.write(str([
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
                targeted_node['name']]) + "\n")
            ptn.delete_vertices(targeted_node)  # delete node
            counter += 1
            if counter >= interactions:
                break


def attack_node_random(file_input, rho):
    """ Function to perform random attacks to nodes on network based on a random algorithm. Removes the target and
    calculate measures to find the impact of it. Receive a Graph file as first argument and result file as second """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/random_node%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    interactions = 3
    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            all_nodes = ptn.vs()
            index_random = randrange(len(all_nodes))
            random_node = ptn.vs[index_random]  # get node id with max degree
            data_out.write(str([
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
                random_node['name']]) + "\n")
            ptn.delete_vertices(random_node)  # delete node
            counter += 1
            if counter >= interactions:
                break


def attack_link_targeted(file_input, rho):
    """ Function to perform targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/target_link%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    interactions = 3
    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            targeted_link = ptn.vs(_degree=ptn.maxdegree())  # get node id with max degree
            data_out.write(str([
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
                targeted_link['route']]) + "\n")
            ptn.delete_vertices(targeted_link)  # delete node
            counter += 1
            if counter >= interactions:
                break

graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net0.graphml"
rho = "0"

attack_node_targeted(graph, rho)
attack_node_random(graph, rho)
