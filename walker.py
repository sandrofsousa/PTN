import random

file_from = "C:\\Users\\Rolf\\Documents\\GitHub\\ptn_model\\edge_list_sample.txt"
steps = 0
nodes_id = []
out_neighbors = []
in_neighbors = []
actual_node = -1
unvisited_list = []

def load_nodes_and_neighborhood_from_file(file_name, weighted = True):
    node_list = []
    out_neighbors_list = []
    in_neighbors_list = []
    with open(file_name) as file_edges:
        for line in file_edges:
            edge_info = line.strip().split(',')
            _has_1st_node = (edge_info[0] in node_list)
            _has_2nd_node = (edge_info[1] in node_list)
            if _has_1st_node and _has_2nd_node:
                if weighted:
                    out_neighbors_list[node_list.index(edge_info[0])].append(node_list.index(edge_info[1]))
                    in_neighbors_list[node_list.index(edge_info[1])].append(node_list.index(edge_info[0]))
                else:
                    if not (node_list.index(edge_info[1]) in out_neighbors_list[node_list.index(edge_info[0])]):
                        out_neighbors_list[node_list.index(edge_info[0])].append(node_list.index(edge_info[1]))
                    if not (node_list.index(edge_info[0]) in in_neighbors_list[node_list.index(edge_info[1])]):
                        in_neighbors_list[node_list.index(edge_info[1])].append(node_list.index(edge_info[0]))
            elif _has_2nd_node:
                node_list.append(edge_info[0])
                out_neighbors_list.append([node_list.index(edge_info[1])])
                in_neighbors_list.append([])
                if weighted:
                    in_neighbors_list[node_list.index(edge_info[1])].append(node_list.index(edge_info[0]))
                else:
                    if not (node_list.index(edge_info[0]) in in_neighbors_list[node_list.index(edge_info[1])]):
                        in_neighbors_list[node_list.index(edge_info[1])].append(node_list.index(edge_info[0]))
            elif _has_1st_node:
                node_list.append(edge_info[1])
                out_neighbors_list.append([])
                in_neighbors_list.append([node_list.index(edge_info[0])])
                if weighted:
                    out_neighbors_list[node_list.index(edge_info[0])].append(node_list.index(edge_info[1]))
                else:
                    if not (node_list.index(edge_info[1]) in out_neighbors_list[node_list.index(edge_info[0])]):
                        out_neighbors_list[node_list.index(edge_info[0])].append(node_list.index(edge_info[1]))
            else:
                node_list.append(edge_info[0])
                node_list.append(edge_info[1])
                out_neighbors_list.append([node_list.index(edge_info[1])])
                in_neighbors_list.append([])
                out_neighbors_list.append([])
                in_neighbors_list.append([node_list.index(edge_info[0])])
        file_edges.close()
    return node_list, out_neighbors_list, in_neighbors_list

def setup():
    global steps, nodes_id, out_neighbors, in_neighbors, unvisited_list, actual_node
    steps = 0
    nodes_id, out_neighbors, in_neighbors = load_nodes_and_neighborhood_from_file(file_from)
    actual_node = random.randint(0, len(nodes_id) - 1)
    unvisited_list = nodes_id

def step():
    global steps, nodes_id, out_neighbors, in_neighbors, unvisited_list, actual_node
    if actual_node in unvisited_list: unvisited_list.remove(actual_node)
    if (len(out_neighbors[actual_node]) > 0) and (len(unvisited_list) > 0):
        actual_node = random.choice(out_neighbors[actual_node])
        steps += 1
        return True
    else: return False

def print_state():
    global steps, nodes_id, out_neighbors, in_neighbors, unvisited_list, actual_node
    print nodes_id[actual_node], [nodes_id[_neighbor] for _neighbor in out_neighbors[actual_node]]

setup()
print_state()
