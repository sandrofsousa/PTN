file_from = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times target.txt"
file_to = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/weighted_network.txt"
edges = []
weights = []
with open(file_from, "r") as edge_file, open(file_to, "w") as weighted_edge_file:
    for line in edge_file:
        if (line in edges):
            weights[edges.index(line)] += 1
        else:
            edges.append(line)
            weights.append(1)
    weighted_edge_file.writelines([edges[i][:-1] + "," + str(weights[i]) + "\n" for i in xrange(len(edges))])
    edge_file.close()
    weighted_edge_file.close()
