import networkx as nx
import matplotlib.pyplot as plt

# # Regular Connected
# G = nx.connected_watts_strogatz_graph(10, 4, 0, seed=None)
# nx.draw_circular(G, node_color='lightgrey', node_size=2000, dpi=221, font_size=20, with_labels=True)
# plt.show()

# # Random graph
# G = nx.erdos_renyi_graph(10, 0.7, seed=None)
# nx.draw_circular(G, node_color='lightgrey', node_size=2000, dpi=221, font_size=20, with_labels=True)
# plt.show()

# Small World
# G = nx.watts_strogatz_graph(10, 4, 0.2)
# nx.draw_circular(G, node_color='lightgrey', node_size=2000, dpi=221, font_size=20, with_labels=True)
# plt.show()

# # Scale free
# G = nx.barabasi_albert_graph(10, 1, 0.4)
# nx.draw_circular(G, node_color='lightgrey', node_size=2000, dpi=221, font_size=20, with_labels=True)
# plt.show()
