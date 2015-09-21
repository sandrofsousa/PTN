__author__ = 'sandrofsousa'

source_file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
target_file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/weighted_network_count.txt"

# Function to read edge list and create a weighted network from counting the frequency of a pair of nodes


def calculate_edges_weight(file_from, file_to):
    edges = []
    weights = []
    with open(file_from, "r") as edge_file, open(file_to, "w") as weighted_edge_file:
        for line in edge_file:
            if line in edges:
                weights[edges.index(line)] += 1
            else:
                edges.append(line)
                weights.append(1)
        weighted_edge_file.writelines([edges[i][:-1] + "," + str(weights[i]) + "\n" for i in range(len(edges))])
        edge_file.close()
        weighted_edge_file.close()

# calculate_edges_weight(source_file, target_file)

# TODO generate weight from distance between nodes

# TODO generate weight based on system capacity

# TODO Generate weight from travel time


# --------------------------------------------------

# Function to create a Weigthed Digraph from edge list containing weights
import networkx as nx


def generate_graph_from_file(file_name):
    global PTN_D
    el = open(file_name, 'rb')
    PTN_D = nx.read_edgelist(el, delimiter=',', create_using=nx.DiGraph(), data=(('weight', int),))
    el.close()

generate_graph_from_file(target_file)

# print(nx.info(PTN_D))
# print(nx.get_edge_attributes(PTN_D, 'weight'))
nx.connected_components(PTN_D)
print(nx.clustering(PTN_D))
