__author__ = 'sandrofsousa'

from csv import reader
from math import sin, cos, sqrt, atan2, radians
from igraph import *
import statistics as sts
from tqdm import tqdm


def get_stops_coordinates():
    """
    Function to read GTFS file as input and get latitude and longitude from stops using a simple parsing,
    output a list with all stops and its respective coordinates.
    """
    file = "gtfs/stops.txt"
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
    stop_times = "gtfs/stop_times.txt"
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
    result = "result/radius_0to200.txt"
    with open(result, "w") as target:
        for rho in tqdm(radius):

            neighbors = get_neighbors(rho, geodata)
            # Save neighbors dict to file for further verification. File's name with text variable for current rho.
            file1 = "result/neighbor%s.txt" % str(rho)
            with open(file1, "w") as data1:
                data1.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in neighbors.items()))

            grouped = group_stops(neighbors)
            # Save grouped dictionary to file for further verification. File's name with text variable for current rho.
            file2 = "result/grouped%s.txt" % str(rho)
            with open(file2, "w") as data2:
                data2.write('\n'.join('{},{}'.format(x2[0], x2[1]) for x2 in grouped.items()))

            times = update_stop_times(grouped)

            edges = create_edge_list(times)
            # Save edge lists to file for further verification. File's name with text variable for current rho.
            file3 = "result/edges%s.txt" % str(rho)
            with open(file3, "w") as data3:
                data3.write('\n'.join('{},{},{}'.format(x3[0], x3[1], x3[2]) for x3 in edges))

            # Create graph from list of tuples.
            ptn = Graph.TupleList(edges, directed=True, vertex_name_attr="name", edge_attrs="trip")
            ptn["name"] = "PTN Sao Paulo, rho: %s" % str(rho)

            # This line will remove self loops, a True assign set for deletion
            ptn.simplify(multiple=False, loops=True, combine_edges=None)

            # Compute graph metrics and save results to file
            loops = False
            target.write(','.join(map(str, [
                rho,                                                   # Rho value
                ptn.vcount(),                                          # Total nodes
                ptn.ecount(),                                          # Total links
                ptn.maxdegree(vertices=None, mode=ALL, loops=loops),   # Max degree
                ptn.diameter(directed=True, unconn=True),              # Network diameter
                sts.mean(ptn.degree(mode=ALL, loops=loops)),           # Mean degree ALL
                sts.mean(ptn.degree(mode=IN, loops=loops)),            # Mean degree IN
                sts.mean(ptn.degree(mode=OUT, loops=loops)),           # Mean degree OUT
                sts.median(ptn.degree(mode=ALL, loops=loops)),         # Median degree ALL
                sts.median(ptn.degree(mode=IN, loops=loops)),          # Median degree IN
                sts.median(ptn.degree(mode=OUT, loops=loops)),         # Median degree OUT
                sts.pvariance(ptn.degree(mode=ALL, loops=loops)),      # Variance deviation ALL
                sts.pstdev(ptn.degree(mode=ALL, loops=loops)),         # Standard deviation ALL
                ptn.average_path_length(directed=True, unconn=True),   # Avg path length
                len(ptn.clusters(mode=WEAK)),                          # Number of clusters WEAK
                len(ptn.clusters(mode=STRONG)),                        # Number of clusters STRONG
                ptn.assortativity_degree(directed=True),               # Assortativity
                ptn.transitivity_undirected(),                         # Clustering coefficient
                str(ptn.density()) + '\n'])))                          # Network Density

            # Write histograms and degrees to file for further analysis.
            histogram = list(ptn.degree_distribution(bin_width=1, mode="all", loops=loops).bins())
            degree_seq = list(ptn.degree(mode=ALL, loops=loops))
            file4 = "result/histogram%s.txt" % str(rho)
            file5 = "result/degree%s.txt" % str(rho)
            with open(file4, "w") as data4, open(file5, "w") as data5:
                data4.write('\n'.join('{},{},{}'.format(x4[0], x4[1], x4[2]) for x4 in histogram))
                data5.write('\n'.join('{}'.format(x5) for x5 in degree_seq))

            #  Write path length histogram do file for further analysis.
            path_hist = list(ptn.path_length_hist(directed=True).bins())
            file6 = "result/path%s.txt" % str(rho)
            with open(file6, "w") as data6:
                data6.write('\n'.join('{},{},{}'.format(x6[0], x6[1], x6[2]) for x6 in path_hist))

            # Write graphml file for network recreation.
            file7 = "result/net%s.graphml" % str(rho)
            ptn.write_graphml(file7)


def write_file():
    """
    Auxiliary function to write results on local files for validation with a fixed radius.
    run time 6.991623584429423 min
    """
    rho = 0
    file1 = "result/geodata%s.txt" % str(rho)
    geodata = get_stops_coordinates()
    with open(file1, "w", newline='') as data1:
        data1.write('\n'.join('{},{},{}'.format(x1[0], x1[1], x1[2]) for x1 in geodata))

    file2 = "result/neighbors%s.txt" % str(rho)
    neighbors = get_neighbors(rho, geodata)
    with open(file2, "w", newline='') as data2:
        data2.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in neighbors.items()))

    file3 = "result/grouped%s.txt" % str(rho)
    grouped = group_stops(neighbors)
    with open(file3, "w", newline='') as data3:
        data3.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in grouped.items()))

    file4 = "result/times%s.txt" % str(rho)
    times = update_stop_times(grouped)
    with open(file4, "w", newline='') as data4:
        data4.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in times))

    file5 = "result/edges%s.txt" % str(rho)
    edges = create_edge_list(times)
    with open(file5, "w", newline='') as data5:
        data5.write('\n'.join('{},{},{}'.format(x1[0], x1[1], x1[2]) for x1 in edges))


main()
