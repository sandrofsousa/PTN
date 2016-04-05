from igraph import *


# # Directed graph
# g = Graph(directed=True)
# g.add_vertices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# g.add_edges([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 9), (0, 2), (0, 8),
#             (1, 9), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9)])
# layout = g.layout_circle()
# plot(g,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_directed.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # Multiple graph
# g5 = Graph()
# g5.add_vertices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# g5.add_edges([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 8), (8, 9), (0, 9), (0, 2), (0, 8),
#             (1, 9), (1, 3), (2, 4), (3, 5), (6, 8), (7, 9), (9, 9), (5, 6), (5, 6), (5, 6)])
# layout = g5.layout_circle()
# plot(g5,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_multiple.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g5.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# Regular connected
# g1 = Graph.Watts_Strogatz(dim=1, size=10, nei=2, p=0, loops=False, multiple=False)
# layout = g1.layout_circle()
# plot(g1,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_regular_connected.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g1.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # Random - Erdos Renyi
# g2 = Graph.Erdos_Renyi(n=10, p=0.7, directed=False, loops=False)
# layout = g2.layout_circle()
# plot(g2,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_random.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g2.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # Small World - Watts Strogatz
# g3 = Graph.Watts_Strogatz(dim=1, size=10, nei=2, p=0.2, loops=False, multiple=False)
# layout = g3.layout_circle()
# plot(g3,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_small_world.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g3.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # Scale Free - Barabasi Albert
# g4 = Graph.Barabasi(n=10, power=2, zero_appeal=1, implementation="psumtree", start_from=None)
# layout = g4.layout_circle()
# plot(g4,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_scale_free1.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g4.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))
