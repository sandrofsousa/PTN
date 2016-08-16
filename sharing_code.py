__author__ = 'sandrofsousa'

from csv import reader
from math import sin, cos, sqrt, atan2, radians
from igraph import *
from time import time
import statistics as sts
from tqdm import tqdm

start = time()

"""
#  ----------------- CODE FOR GROUPING PROCESS AND GRAPH GENERATION -----------------

Suggested folder structure for code execution, some changes could be required:

\
/gtfs/      - GTFS files to be analysed     (required)
/neighbors/ - Neighbors dictionaries        (optional)
/groups/    - Grouped dictionaries          (optional)
/edges/     - Edge lists and grapml files   (required)
/histograms - Degree histograms             (optional)
/degrees/   - Degree Sequences              (optional)
/paths/     - Path length histograms        (optional)
/attacks/   - Attacks results               (required)

"""


def get_stops_coordinates():
    """
    Function to read GTFS file as input and get latitude and longitude from stops using a simple parsing,
    output a list with all stops and its respective coordinates.
    """
    file = "/gtfs/stops.txt"
    geodata = []
    with open(file, "r", newline='') as data:
        searcher = reader(data, delimiter=',', quotechar='"')  # Parse data using csv based on ',' position
        next(searcher)  # Skip first line (header)
        for line in searcher:  # Select the respective column of line based on ',' position
            stop_id = int(line[0])
            stop_lat = float(line[3])
            stop_lon = float(line[4])
            geodata.append((stop_id, stop_lat, stop_lon))  # Append fields from line to geodata list
        data.close()
    return geodata


def distance_on_sphere(lat1, lon1, lat2, lon2):
    """
    Auxiliary function to calculate distance on sphere in meters from two latitude and longitude pars,
    output the distance in meters of two given coordinates. based on John D. Cock algorithm.
    """
    r = 6371007.176   # Approximate mean radius of earth in meters
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])  # Convert decimal degrees to radians
    # Compute difference from variables
    dif_lat = lat2 - lat1
    dif_lon = lon2 - lon1

    # Haversine formula to calculate the great-circle distance between two points
    a = sin(dif_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c
    return distance


def get_neighbors(radius, stops_list):
    """
    Function to search stops near each other (neighbors). A radius value and a list of stops with coordinates
    are passed as input. A stop is classified as neighbor if the distance is lower than the radius, outputing
    a dictionary with stop as key and IDs of its neighbors.
    """
    neighbors = dict()
    for row in range(len(stops_list)):  # Populate dictionary with keys and empty values for content
        stop = stops_list[row][0]
        neighbors[stop] = []

    if radius == 0:
        return neighbors
    else:
        for row1 in range(len(stops_list) - 1):  # Loop reading the list of stops, positioning in the first line of file
            stop1 = stops_list[row1][0]  # Get values from first row.
            lat1 = stops_list[row1][1]
            lon1 = stops_list[row1][2]

            for row2 in range(row1 + 1, len(stops_list)):  # Read value of stops list, getting the position from row1.
                stop2 = stops_list[row2][0]  # Get values from second row.
                lat2 = stops_list[row2][1]
                lon2 = stops_list[row2][2]
                distance = distance_on_sphere(lat1, lon1, lat2, lon2)  # Calculate the distance between stops.
                # If distance <= rho, update dictionary for respective keys (stop2 is neighbor of stop1, reciprocal).
                if distance <= radius:
                    neighbors[stop1].append(stop2)
                    neighbors[stop2].append(stop1)
                else:
                    continue
        return neighbors


def recursive_search(series, aux_list, neighbors_dict):
    """
    Auxiliary recursive function to get neighbors of respective stop and search for neighbors of each element
    of the list. It return a list with the cluster of neighbors grouped linearly.
    """
    for stop in aux_list:  # For element in the list of neighbors, search for it' own neighbors and increment aux_list.
        if stop not in series:
            series.append(stop)
            rec_stop = neighbors_dict[stop]
            aux_list += rec_stop
            return recursive_search(series, aux_list, neighbors_dict)  # Call function again for each neighbor found.
        else:
            continue
    return series


def group_stops(neighbors_dict):
    """
    Function to process neighbors IDs(dictionary) and replace them with a new id for stops that are
    close each other based on radius value.
    """
    grouped = {}
    last_id = 0
    # For each item in neighbors_dict, fill series list with stop to be analysed and aux list with it's neighbors.
    for item in neighbors_dict:
        if item in grouped:                 # Id already parsed, ignore.
            continue
        series = [item]                     # Initialize list with stop to be searched.
        aux_list = neighbors_dict[item]     # Populate list with neighbors of stops
        cluster = recursive_search(series, aux_list, neighbors_dict)  # Search recursively any element of series

        for stop in cluster:  # Set the same new ID for all elements of the cluster
            grouped[stop] = "v" + str(last_id + 1)
        last_id += 1    # update last_id list to keep consistent sequence
    return grouped


def update_stop_times(grouped_dict):
    """
    Read stop_times file and replace the current stop_id on route sequence with new id from grouped dictionary.
    """
    stop_times = "/gtfs/stop_times.txt"
    new_stop_times = []
    with open(stop_times, "r", newline='') as times:
        searcher = reader(times, delimiter=',', quotechar='"')  # Parse data using csv based on ',' position.
        next(searcher)  # Skip header (first line).
        for line in searcher:
            trip_id = str(line[0])  # Select columns based on ',' position and update list serially.
            stop_id = int(line[3])
            new_stop_times.append((trip_id, str(grouped_dict[stop_id])))  # Update list based on grouped dict keys
    return new_stop_times


def create_edge_list(times_list):
    """
    Function to create edge list from stop_times file with new IDs, taking the first stop of sequence
    and saving the next stop as its successor for any line where the trip is the same.
    """
    edge_list = []
    for row in range(0, len(times_list) - 1):  # Start index at 0 and finish at last line from list
        trip1 = times_list[row][0]
        stop1 = times_list[row][1]
        trip2 = times_list[row + 1][0]   # Get trip_id from next line
        stop2 = times_list[row + 1][1]   # Get stop_id from next line
        if trip1 == trip2:  # Create a link only if the stops are in the same line sequence
            edge_list.append((str(stop1), str(stop2), str(trip1)))
    return edge_list


def main():
    """
    Main function to process gtfs sub-functions given a vector of radius values.
    For any value of radius, save the grouped dictionary and edge list used to create the graph.
    Returns a file with histograms for any radius and network statistics. Run time 303.97410554885863 (5.6hs)
    """
    geodata = get_stops_coordinates()
    radius = list(range(0, 205, 5))
    result = "/radius_0to200.txt"
    with open(result, "w") as target:
        for rho in tqdm(radius):

            neighbors = get_neighbors(rho, geodata)
            # Save neighbors dict to file for further verification. File's name with text variable for current rho.
            file1 = "/neighbors/neighbor%s.txt" % str(rho)
            with open(file1, "w") as data1:
                data1.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in neighbors.items()))

            grouped = group_stops(neighbors)
            # Save grouped dictionary to file for further verification. File's name with text variable for current rho.
            file2 = "/groups/grouped%s.txt" % str(rho)
            with open(file2, "w") as data2:
                data2.write('\n'.join('{},{}'.format(x2[0], x2[1]) for x2 in grouped.items()))

            times = update_stop_times(grouped)

            edges = create_edge_list(times)
            # Save edge lists to file for further verification. File's name with text variable for current rho.
            file3 = "/edges/edges%s.txt" % str(rho)
            with open(file3, "w") as data3:
                data3.write('\n'.join('{},{},{}'.format(x3[0], x3[1], x3[2]) for x3 in edges))

            # Create graph from list of tuples.
            ptn = Graph.TupleList(edges, directed=True, vertex_name_attr="name", edge_attrs="trip")
            ptn["name"] = "PTN Sao Paulo, rho: %s" % str(rho)

            # Perform respective graph calculation and save to file
            target.write(str([
                rho,                                                  # Rho value
                ptn.vcount(),                                         # Total nodes
                ptn.ecount(),                                         # Total links
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),   # Max degree
                ptn.diameter(directed=True, unconn=True),             # Network diameter
                sts.mean(ptn.degree(mode=ALL, loops=True)),           # Mean degree ALL
                sts.mean(ptn.degree(mode=IN, loops=True)),            # Mean degree IN
                sts.mean(ptn.degree(mode=OUT, loops=True)),           # Mean degree OUT
                sts.median(ptn.degree(mode=ALL, loops=True)),         # Median degree ALL
                sts.median(ptn.degree(mode=IN, loops=True)),          # Median degree IN
                sts.median(ptn.degree(mode=OUT, loops=True)),         # Median degree OUT
                sts.pvariance(ptn.degree(mode=ALL, loops=True)),      # Variance deviation ALL
                sts.pstdev(ptn.degree(mode=ALL, loops=True)),         # Standard deviation ALL
                ptn.average_path_length(directed=True, unconn=True),  # Avg path length
                len(ptn.clusters(mode=WEAK)),                         # Number of clusters WEAK
                len(ptn.clusters(mode=STRONG)),                       # Number of clusters STRONG
                ptn.assortativity_degree(directed=True),              # Assortativity
                ptn.transitivity_undirected(),                        # Clustering coefficient
                ptn.density()]) + "\n")                               # Network Density

            # Write histograms and degrees to file for further analysis.
            histogram = list(ptn.degree_distribution(bin_width=1, mode="all", loops=True).bins())
            degree_seq = list(ptn.degree(mode=ALL, loops=True))
            file4 = "/histogram/hist%s.txt" % str(rho)
            file5 = "/degrees/deg%s.txt" % str(rho)
            with open(file4, "w") as data4, open(file5, "w") as data5:
                data4.write('\n'.join('{},{},{}'.format(x4[0], x4[1], x4[2]) for x4 in histogram))
                data5.write('\n'.join('{}'.format(x5) for x5 in degree_seq))

            #  Write path length histogram do file for further analysis.
            path_hist = list(ptn.path_length_hist(directed=True).bins())
            file6 = "/paths/path%s.txt" % str(rho)
            with open(file6, "w") as data6:
                data6.write('\n'.join('{},{},{}'.format(x6[0], x6[1], x6[2]) for x6 in path_hist))

            # Write graphml file for network recreation.
            file7 = "/edges/net%s.graphml" % str(rho)
            ptn.write_graphml(file7)

main()

end = time()
elapsed = ((end - start) / 60) / 60
print("Run time: " + str(elapsed))

"""
#  ----------------- CODE FOR ATTACK SIMULATIONS -----------------

# __author__ = 'sandrofsousa'

# from igraph import *
# from random import choice
# from time import time
# from tqdm import tqdm
"""

start = time()


def attack_node_targeted(file_input, rho, interactions):
    """
    Function to perform deterministic targeted attacks on network based on a node importance (degree).
    Removes the target (max degree on network) and calculate global measures to find the impact of it.
    Graph file, rho value and number of interactions are passed as input arguments, result on a file as output.
    """
    file_output = "/attacks/node_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0         # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while counter <= interactions:                                # stop if counter reach interactions limit
            targeted_list = ptn.vs(_degree=ptn.maxdegree(vertices=None, mode=ALL, loops=True))['name']
            for targeted_node in targeted_list:                       # loop at nodes if more than one has same degree
                data_out.write(str([
                    counter,
                    ptn.vcount(),
                    ptn.ecount(),
                    ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                    ptn.diameter(directed=True, unconn=True),
                    ptn.average_path_length(directed=True, unconn=True),
                    len(ptn.clusters(mode=WEAK)),
                    len(ptn.clusters(mode=STRONG)),
                    ptn.assortativity_degree(directed=True),
                    ptn.transitivity_undirected(),
                    ptn.density(),
                    targeted_node]) + "\n")
                ptn.delete_vertices(ptn.vs.find(name=targeted_node))  # delete node
                counter += 1                                          # increase counter
                if counter > interactions:
                    break


def attack_node_targeted_prob(file_input, rho, interactions):
    """
    Function to perform probabilistic targeted attacks on network based on a node probability (degree). Removes the
    target and calculate global measures to find the impact of it. Graph file, rho value and
    number of interactions are passed as input arguments, result on a file as output.
    """
    file_output = "/attacks/node_probab%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    nodes_probability = []                          # probability based on node repetition on list
    for node in ptn.vs:                             # populate a list repeating node_name n times it's degree.
        for i in range(node.degree()):
            nodes_probability.append(node["name"])

    counter = 0                                    # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while True:                                # stop if counter reach interactions limit
            targeted_node = choice(nodes_probability)   # choose a node randomly by probability list
            data_out.write(str([
                counter,
                ptn.vcount(),
                ptn.ecount(),
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                ptn.diameter(directed=True, unconn=True),
                ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                targeted_node]) + "\n")
            ptn.delete_vertices(ptn.vs.find(name=targeted_node))  # delete node
            counter += 1                                          # increase counter

            for i in nodes_probability:
                nodes_probability.remove(targeted_node)           # remove node from probability list
                if targeted_node not in nodes_probability:
                    break

            if counter > interactions:
                break


def attack_node_random(file_input, rho, interactions):
    """
    Function to perform random attacks on network based on a random choice. Removes the target (random) and
    calculate global measures to find the impact of it. Graph file, rho value and number of interactions are
    passed as input arguments, result on a file as output.
    """
    file_output = "/attacks/node_random%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0         # update every time a node is deleted
    with open(file_output, "w") as data_out:
        while True:
            all_nodes = ptn.vs()['name']             # get all nodes
            random_node = choice(all_nodes)          # return a random node from list
            data_out.write(str([
                counter,
                ptn.vcount(),
                ptn.ecount(),
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                ptn.diameter(directed=True, unconn=True),
                ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                random_node]) + "\n")
            ptn.delete_vertices(ptn.vs.find(name=random_node))  # delete node
            counter += 1                                        # increase counter
            if counter > interactions:
                break


def attack_link_targeted(file_input, rho, interactions):
    """
    Function to perform deterministic targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file, rho value and number of interactions are
    passed as input arguments, result on a file as output.
    """
    file_output = "/attacks/link_target%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    for idx, edge in enumerate(ptn.es):             # add weights to edges based on their multiplicity on network
        edge["weight"] = ptn.count_multiple(idx)

    edge_id = 0
    for idx, edge in enumerate(ptn.es):             # create an attribute edge_id to avoid index rebuild by igraph
        edge["edge_id"] = "e" + str(edge_id + 1)
        edge_id += 1

    counter = 0
    with open(file_output, "w") as data_out:
        while counter <= interactions:
            max_weight = max(ptn.es['weight'])
            targeted_list = ptn.es(weight=max_weight)['edge_id']  # get edge with max multiplicity
            for targeted_link in targeted_list:  # loop at nodes if more than one has same degree
                data_out.write(str([
                    counter,
                    ptn.vcount(),
                    ptn.ecount(),
                    ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                    ptn.diameter(directed=True, unconn=True),
                    ptn.average_path_length(directed=True, unconn=True),
                    len(ptn.clusters(mode=WEAK)),
                    len(ptn.clusters(mode=STRONG)),
                    ptn.assortativity_degree(directed=True),
                    ptn.transitivity_undirected(),
                    ptn.density(),
                    ptn.es(edge_id=targeted_link)['weight'],
                    targeted_link]) + "\n")
                ptn.delete_edges(ptn.es.find(edge_id=targeted_link))  # delete node
                counter += 1  # increase counter
                if counter >= interactions:
                    break


def attack_link_targeted_prob(file_input, rho, interactions):
    """
    Function to perform probabilistic targeted attacks on network based on a link probability. Removes the target
    and calculate measures to find the impact of it. Graph file, rho value and number of interactions are
    passed as input argument, result on a file as output.
    """
    file_output = "/attacks/link_probab%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)

    for idx, edge in enumerate(ptn.es):             # add weights to edges based on their multiplicity on network
        edge["weight"] = ptn.count_multiple(idx)

    edge_id = 0
    for idx, edge in enumerate(ptn.es):             # create an attribute edge_id to avoid index rebuild by igraph
        edge["edge_id"] = "e" + str(edge_id + 1)    # update edge dictionary
        edge_id += 1

    links_probability = []                          # probability based on link repetition on list
    for link in ptn.es:                             # populate a list repeating edge_id n times it's weight.
        for i in range(link["weight"]):
            links_probability.append(link["edge_id"])

    counter = 0
    with open(file_output, "w") as data_out:
        while True:
            targeted_link = choice(links_probability)   # choose a link randomly from probability list
            data_out.write(str([
                counter,
                ptn.vcount(),
                ptn.ecount(),
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                ptn.diameter(directed=True, unconn=True),
                ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                ptn.es(edge_id=targeted_link)['weight'],
                targeted_link]) + "\n")
            ptn.delete_edges(ptn.es.find(edge_id=targeted_link))  # delete node
            counter += 1  # increase counter

            for i in links_probability:
                links_probability.remove(targeted_link)           # remove link from probability list
                if targeted_link not in links_probability:
                    break

            if counter >= interactions:
                break


def attack_link_random(file_input, rho, interactions):
    """
    Function to perform targeted attacks on network based on a link importance. Removes the target
    and calculate measures to find the impact of it. Graph file, rho value and number of interactions are
    passed as input argument, result on a file as output.
    """
    file_output = "/attacks/link_random%s.txt" % rho
    ptn = Graph.Read_GraphML(file_input)
    counter = 0
    with open(file_output, "w") as data_out:
        while True:                  # stop if counter reach interactions limit
            all_edges = ptn.es()                        # get all edges
            random_link = choice(all_edges)          # return edge id based on index
            data_out.write(str([
                counter,
                ptn.vcount(),
                ptn.ecount(),
                ptn.maxdegree(vertices=None, mode=ALL, loops=True),
                ptn.diameter(directed=True, unconn=True),
                ptn.average_path_length(directed=True, unconn=True),
                len(ptn.clusters(mode=WEAK)),
                len(ptn.clusters(mode=STRONG)),
                ptn.assortativity_degree(directed=True),
                ptn.transitivity_undirected(),
                ptn.density(),
                random_link['trip']]) + "\n")
            ptn.delete_edges(random_link)   # delete edge
            counter += 1                    # increase counter
            if counter > interactions:
                break


def cut_articulation_points():
    file_output = "/attacks/cuts.txt"
    radius = list(range(0, 205, 5))
    with open(file_output, "w") as result:
        for rho in radius:
            graph = "/edges/net%s.graphml" % rho
            ptn = Graph.Read_GraphML(graph)
            articulation_points = ptn.cut_vertices()
            listing = list(ptn.vs[v]["name"] for v in articulation_points)
            result.write(str(rho) + "," + str(listing) + "\n")


def attack_scenarios():
    """
    Function to run all attack scenarios for different values of rho processed before. It controls the networks
    to be analysed and the number of interactions the delete process will be removing nodes or links.
    Run time: 41.11158872803052 hs
    """
    radius = [0, 20, 65, 150, 200]
    interactions = 200

    for rho in tqdm(radius):
        graph = "/edges/net%s.graphml" % rho            # replace file name with rho value from loop
        attack_node_targeted(graph, rho, interactions)
        attack_node_targeted_prob(graph, rho, interactions)
        attack_node_random(graph, rho, interactions)
        attack_link_targeted(graph, rho, interactions)
        attack_link_targeted_prob(graph, rho, interactions)
        attack_link_random(graph, rho, interactions)
    cut_articulation_points()

attack_scenarios()

end = time()
elapsed = ((end - start) / 60) / 60
print("Run time: " + str(elapsed))
