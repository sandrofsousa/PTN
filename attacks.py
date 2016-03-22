__author__ = 'sandrofsousa'

from igraph import *
from csv import reader

# Actual graph with rho 0 for validation
file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/edges0.txt"
edges = []

with open(file, "r", newline='') as data:
    # Parse data using csv based on ',' position.
    searcher = reader(data, delimiter=',', quotechar='"')
    for line in searcher:
        # Select the respective column of line based on ',' position.
        source = line[0]
        target = line[1]
        route = line[2]

        # Append fields from line to geodata list
        edges.append((source, target, route))

    data.close()

ptn = Graph.TupleList(edges, directed=False, vertex_name_attr="name", edge_attrs="route")
ptn["name"] = "PTN Sao Paulo rho0"
summary(ptn)
