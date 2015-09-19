__author__ = 'sandrofsousa'

source = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edge_list.txt"
el = open(source, 'rb')
PTN_D = nx.read_edgelist(el, delimiter=',', create_using=nx.DiGraph())
el.close()