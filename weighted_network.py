__author__ = 'sandrofsousa'

# TODO generate weight from link count

source_file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
target_file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/weighted_network.txt"


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
        weighted_edge_file.writelines([edges[i][:-1] + "," + "weight=" + str(weights[i]) + "\n" for i in range(len(edges))])
        edge_file.close()
        weighted_edge_file.close()

calculate_edges_weight(source_file, target_file)

# TODO generate weight from distance between nodes

# TODO generate weight based on system capacity

# TODO Generate weight from travel time



