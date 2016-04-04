from igraph import *


# # # Samll World - Watts Strogatz
# g1 = Graph.Watts_Strogatz(dim=1, size=10, nei=2, p=0, loops=False, multiple=False)
# layout = g1.layout_circle()
# plot(g1,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_regular_connected.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # # Random - Erdos Renyi
# g2 = Graph.Erdos_Renyi(n=10, p=0, directed=False, loops=False)
# layout = g2.layout_circle()
# plot(g2,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_random.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))


# # # Scale Free - Barabasi
# g2 = Graph.Erdos_Renyi(n=10, p=0, directed=False, loops=False)
# layout = g2.layout_circle()
# plot(g2,
#      "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/Latex/fig/graph_random.pdf",
#      layout=layout,
#      vertex_color="rgb(210, 210, 210)",
#      vertex_size=28,
#      vertex_label=g.vs.indices,
#      vertex_label_size=12,
#      bbox=(330, 330))