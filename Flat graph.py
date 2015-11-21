# Grafos gerados para qualificacão

import networkx as nx
import matplotlib.pyplot as plt

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
#
# from networkx import *
# import matplotlib.pyplot as plt
#
#
# z=[1,1,2,3,5,8,13]
# print(is_valid_degree_sequence(z))
#
# print("Configuration model")
# G=configuration_model(z)  # configuration model
# degree_sequence=list(degree(G).values()) # degree sequence
# print("Degree sequence %s" % degree_sequence)
# print("Degree histogram")
# hist={}
# for d in degree_sequence:
#     if d in hist:
#         hist[d]+=1
#     else:
#         hist[d]=1
# print("degree #nodes")
# for d in hist:
#     print('%d %d' % (d,hist[d]))
#
# draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True)
# plt.show()


# Regular Connected
G = nx.connected_watts_strogatz_graph(40, 39, 100)
nx.draw_circular(G, node_color='lightgrey', node_size=800, with_labels=True, link_color='red')
plt.show()