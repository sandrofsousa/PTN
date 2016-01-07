# Grafos gerados para qualificacão

# import networkx as nx
# import matplotlib.pyplot as plt

# # Random graph
# G = nx.erdos_renyi_graph(16, 2)
# nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# # Small World
# G = nx.watts_strogatz_graph(16, 4, 0.2)
# nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# # Regular Connected
# G = nx.connected_watts_strogatz_graph(13, 8, 0)
# nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# # Scale free
# G = nx.barabasi_albert_graph(16, 1, 0.4)
# nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# # Scale free
# G = nx.barabasi_albert_graph(16, 1, 0.4)
# nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# Scale free
# G = nx.Graph()
# G.add_nodes_from([1,2,3,4,5,6,7,8])
# G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 5), (6, 7), (7, 3), (3, 8), (8, 9)])
# nx.draw(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()

# B = nx.Graph()
# B.add_nodes_from([1,2,3,4,5], bipartite=0) # Add the node attribute "bipartite"
# B.add_nodes_from(['a','b','c','d'], bipartite=1)
# B.add_edges_from([(1,2), (2,3), (3,4), (4,5), ('a','b'), ('b',3), (3,'c'), ('c','d')])
# nx.draw(B, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()


from igraph import *

# target = open("/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/ptn_graph.graphml", "r")
# g = Graph.Read_GraphML(target)
# print(Graph.summary(g, verbosity=0))
# print(g.vs['name'])
# # trip = g.es.find(trip="1016-10-0")
# # print(trip)
# # print("type:", type(trip), "trip:", trip.index)


# TODO search vertex by name of stops
# TODO Select metrics to process
# TODO Test metrics

# g = Graph([(0,1), (0,2), (2,3), (3,4), (4,2), (2,5), (5,0), (6,3), (5,6)])
# g.vs["name"] = ["Alice", "Bob", "Claire", "Dennis", "Esther", "Frank", "George"]
# g.vs["age"] = [25, 31, 18, 47, 22, 23, 50]
# g.vs["gender"] = ["f", "m", "f", "m", "f", "m", "m"]
# g.es["is_formal"] = [False, False, True, True, True, False, True, False, False]
# print(g.vs[0].attributes(), g.degree())
# target = open("/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/ptn_graph.graphml", "w")
# Graph.write_graphml(g, target)
