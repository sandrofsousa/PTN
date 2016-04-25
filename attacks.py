__author__ = 'sandrofsousa'

from igraph import *
from random import choice
from time import time
from tqdm import tqdm

start = time()


def attack_node_targeted(file_input, rho, interactions):
    """
    Function to perform deterministic targeted attacks on network based on a node importance (degree).
    Removes the target (max degree on network) and calculate global measures to find the impact of it.
    Graph file, rho value and number of interactions are passed as input argument, result on a file as output.
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/node_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0         # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while counter <= interactions:                                # stop if counter reach interactions limit
            targeted_list = ptn.vs(_degree=ptn.maxdegree(vertices=None, mode=ALL, loops=True))['name']
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
                counter += 1                                          # increase counter
                if counter > interactions:
                    break


def attack_node_targeted_prob(file_input, rho, interactions):
    """
    Function to perform targeted attacks on network based on a node importance (degree). Removes the target
    (max degree on network) and calculate global measures to find the impact of it. Graph file, rho value and
    number of interactions are passed as input argument, result on a file as output.
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/node_probab%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    nodes_probability = []                          # probability based on node repetition on list
    for node in ptn.vs:                             # populate a list repeating node_name n times it's degree.
        for i in range(node.degree()):
            nodes_probability.append(node["name"])

    counter = 0                                    # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while True:                                # stop if counter reach interactions limit
            targeted_node = choice(nodes_probability)   # choose a node randomly by probability list
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
            counter += 1                                          # increase counter

            for i in nodes_probability:
                nodes_probability.remove(targeted_node)           # remove node from probability list
                if targeted_node not in nodes_probability:
                    break

            if counter > interactions:
                break


def attack_node_random(file_input, rho, interactions):
    """
    Function to perform random attacks on network based on a random choise. Removes the target (random) and
    calculate global measures to find the impact of it. Graph file, rho value and number of interactions are
    passed as input argument, result on a file as output.
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
                ptn.diameter(directed=True, unconn=True),
                ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                random_node]) + "\n")
            ptn.delete_vertices(ptn.vs.find(name=random_node))  # delete node
            counter += 1                                        # increase counter
            if counter > interactions:
                break


def attack_link_targeted(file_input, rho, interactions):
    """
    Function to perform deterministic targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/link_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    for idx, edge in enumerate(ptn.es):             # add weights to edges based on their multiplicity on network
        edge["weight"] = ptn.count_multiple(idx)

    edge_id = 0
    for idx, edge in enumerate(ptn.es):             # create an attribute edge_id to avoid index rebuild by igraph
        edge["edge_id"] = "e" + str(edge_id + 1)
        edge_id += 1

    counter = 0
    with open(file_output, "w") as data_out:
        while counter <= interactions:
            max_weight = max(ptn.es['weight'])
            targeted_list = ptn.es(weight=max_weight)['edge_id']  # get edge with max multiplicity
            for targeted_link in targeted_list:  # loop at nodes if more than one has same degree
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
                    ptn.es(edge_id=targeted_link)['weight'],
                    targeted_link]) + "\n")
                ptn.delete_edges(ptn.es.find(edge_id=targeted_link))  # delete node
                counter += 1  # increase counter
                if counter >= interactions:
                    break


def attack_link_targeted_prob(file_input, rho, interactions):
    """
    Function to perform deterministic targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file as first argument and result file as second
    """
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/link_probab%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    for idx, edge in enumerate(ptn.es):             # add weights to edges based on their multiplicity on network
        edge["weight"] = ptn.count_multiple(idx)

    edge_id = 0
    for idx, edge in enumerate(ptn.es):             # create an attribute edge_id to avoid index rebuild by igraph
        edge["edge_id"] = "e" + str(edge_id + 1)    # update edge dictionary
        edge_id += 1

    links_probability = []                          # probability based on link repetition on list
    for link in ptn.es:                             # populate a list repeating edge_id n times it's weight.
        for i in range(link["weight"]):
            links_probability.append(link["edge_id"])

    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            targeted_link = choice(links_probability)   # choose a link randomly from probability list
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
                ptn.es(edge_id=targeted_link)['weight'],
                targeted_link]) + "\n")
            ptn.delete_edges(ptn.es.find(edge_id=targeted_link))  # delete node
            counter += 1  # increase counter

            for i in links_probability:
                links_probability.remove(targeted_link)           # remove link from probability list
                if targeted_link not in links_probability:
                    break

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
        while True:                  # stop if counter reach interactions limit
            all_edges = ptn.es()                        # get all edges
            random_link = choice(all_edges)          # return edge id based on index
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
            if counter > interactions:
                break


def cut_articulation_points():
    file_output = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/attacks/cuts.txt"
    radius = list(range(0, 205, 5))
    with open(file_output, "w") as result:
        for rho in radius:
            graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net%s.graphml" % rho
            ptn = Graph.Read_GraphML(graph)
            articulation_points = ptn.cut_vertices()
            listing = list(ptn.vs[v]["name"] for v in articulation_points)
            result.write(str(rho) + "," + str(listing) + "\n")


def attack_scenarios():
    """
    Function to run all attack scenarios for different values of rho processed before. It controls the networks
    to be analysed and the number of interactions the delete process will be removing nodes or links.
    Run time: 41.11158872803052 hs
    """
    radius = [0, 20, 65, 150, 200]
    interactions = 200

    for rho in tqdm(radius):
        graph = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/net%s.graphml" % rho
        # attack_node_targeted(graph, rho, interactions)
        attack_node_targeted_prob(graph, rho, interactions)
        # attack_node_random(graph, rho, interactions)
        # attack_link_targeted(graph, rho, interactions)
        attack_link_targeted_prob(graph, rho, interactions)
        # attack_link_random(graph, rho, interactions)
    # cut_articulation_points()


# attack_scenarios()

end = time()
elapsed = ((end - start) / 60) / 60
print("Run time: " + str(elapsed))
