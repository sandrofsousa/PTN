file_from = "C:\\Users\\Rolf\\Documents\\GitHub\\ptn_model\\edge_list_sample.txt"
file_to = "C:\\Users\\Rolf\\Documents\\GitHub\\ptn_model\\weighted_edge_list_sample.txt"
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
