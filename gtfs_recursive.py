__author__ = 'sandrofsousa'

# Imports
from csv import reader
from math import sin, cos, sqrt, atan2, radians
from igraph import *
import time

start = time.time()


# Function to read GTFS file and get latitude and longitude from stops using a simple parsing.
def get_stops_coordinates():  # PASSED
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stops.txt"
    geodata = []

    with open(file, "r", newline='') as data:
        # Parse data using csv based on ',' position.
        searcher = reader(data, delimiter=',', quotechar='"')
        # Skip header (first line).
        next(searcher)
        for line in searcher:
            # Select the respective column of line based on ',' position.
            stop_id = int(line[0])
            stop_lat = float(line[3])
            stop_lon = float(line[4])

            # Append fields from line to geodata list
            geodata.append((stop_id, stop_lat, stop_lon))

        data.close()
    return geodata


# Function to calculate distance on sphere in meters from two latitude and longitude pars.
def distance_on_sphere(lat1, lon1, lat2, lon2):  # PASSED
    # Approximate mean radius of earth in meters
    r = 6371007.176

    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Compute difference from variables
    dif_lat = lat2 - lat1
    dif_lon = lon2 - lon1

    # Haversine formula to calculate the great-circle distance between two points
    a = sin(dif_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


# Function to search stops near each other (neighbors). A radius value and a list of stops with coordinates
# are passed. A stop is classified as neighbor if the distance is lower than the radius.
def get_neighbors(radius, stops_list):  # PASSED
    neighbors = dict()

    # Populate dictionary with keys and empty values for content.
    for row in range(len(stops_list)):
        stop = stops_list[row][0]
        neighbors[stop] = []

    # Loop reading the list of stops, positioning in the first line of file.
    for row1 in range(len(stops_list) - 1):
        # Get values from first row.
        stop1 = stops_list[row1][0]
        lat1 = stops_list[row1][1]
        lon1 = stops_list[row1][2]

        # Loop reading the next value of stops list, getting the next row after row1.
        for row2 in range(row1 + 1, len(stops_list)):
            # Get values from second row.
            stop2 = stops_list[row2][0]
            lat2 = stops_list[row2][1]
            lon2 = stops_list[row2][2]

            # Call function to calculate the distance between two stops.
            distance = distance_on_sphere(lat1, lon1, lat2, lon2)

            # If distance <= rho, update dictionary value for the respective key (stop2 is neighbor of stop1).
            if distance <= radius:
                neighbors[stop1].append(stop2)
                neighbors[stop2].append(stop1)
            else:
                continue
    return neighbors


# Recursive function to get neighbors of respective stop and search for neighbors of each element of the list.
# It return a list with the cluster of neighbors joined linearly.
def recursive_search(series, aux_list, neighbors_dict):

    # For element in the list of neighbors, search for it' own neighbors and increment aux_list.
    for stop in aux_list:
        if stop not in series:
            series.append(stop)
            rec_stop = neighbors_dict[stop]
            aux_list += rec_stop
            return recursive_search(series, aux_list, neighbors_dict)    # Call the function again for each neighbor.
        else:
            continue
    return series


# Function to process neighbors IDs(list) from previous algorithm and replace them with a new id for grouped stops.
def group_stops(neighbors_dict):
    grouped = {}
    last_id = 0

    # For each item in neighbors_dict, fill series list with stop to be analysed and aux list with it's neighbors.
    for item in neighbors_dict:
        if item in grouped:                 # Id already parsed, ignore.
            continue

        series = [item]                     # Initialize list with stop to be searched.
        aux_list = neighbors_dict[item]     # Populate list with neighbors of stops

        # Call recursive function to search for neighbors of elements of aux_list
        cluster = recursive_search(series, aux_list, neighbors_dict)

        # Set the same new ID for all elements of the cluster
        for stop in cluster:
            grouped[stop] = "v" + str(last_id + 1)
        last_id += 1    # update last_id list to keep consistent sequence

    return grouped


# Read stop_times file and replace the current stop on route sequence with new id when it exist on grouped dictionary.
def update_stop_times(grouped_dict):
    stop_times = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stop_times.txt"
    new_stop_times = []

    with open(stop_times, "r", newline='') as times:
        # Parse data using csv based on ',' position.
        searcher = reader(times, delimiter=',', quotechar='"')
        # Skip header (first line).
        next(searcher)
        for line in searcher:
            # Select the respective column of line based on ',' position and update list serially.
            trip_id = str(line[0])
            stop_id = int(line[3])
            new_stop_times.append((trip_id, str(grouped_dict[stop_id])))

        # Close file
        times.close()

    return new_stop_times


# Function to create edge list from stop_times file previously updated with new IDs.
def create_edge_list(times_list):
    edge_list = []

    # Start index at 0 and finish at last line from list
    for row in range(0, len(times_list) - 1):
        trip1 = times_list[row][0]
        stop1 = times_list[row][1]
        trip2 = times_list[row + 1][0]   # Get trip_id from next line
        stop2 = times_list[row + 1][1]   # Get stop_id from next line

        # Create a link only if the stops are in the same line sequence
        if trip1 == trip2:
            edge_list.append((str(stop1), str(stop2), str(trip1)))

    return edge_list


# Main function to process gtfs sub-functions given a vector of radius values.
# For any value of radius, save the grouped dictionary and edge list used to create the graph.
# Returns a file with histograms for any radius and network statistics.
def main():
    geodata = get_stops_coordinates()
    radius = list(range(0, 205, 5))
    result = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/radius_0to200.txt"

    with open(result, "w") as target:
        for rho in radius:

            neighbors = get_neighbors(rho, geodata)
            # Save neighbors dict to file for further verification. File's name with text variable for current rho.
            file1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/neighbors/neighbors%s.txt" % str(rho)
            with open(file1, "w", newline='') as data1:
                data1.write("%s\n" % str(line1) for line1 in neighbors)

            grouped = group_stops(neighbors)
            # Save grouped dictionary to file for further verification. File's name with text variable for current rho.
            file2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/groups/grouped%s.txt" % str(rho)
            with open(file2, "w", newline='') as data2:
                data2.write('\n'.join('{},{}'.format(x1[0], x1[1]) for x1 in grouped.items()))

            times = update_stop_times(grouped)

            edges = create_edge_list(times)
            # Save edge lists to file for further verification. File's name with text variable for current rho.
            file3 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/edges%s.txt" % str(rho)
            with open(file3, "w", newline='') as data3:
                data3.write('\n'.join('{},{},{}'.format(x2[0], x2[1], x2[2]) for x2 in edges))

            # Create graph from list of tuples.
            ptn = Graph.TupleList(edges, directed=True, vertex_name_attr="name", edge_attrs="trip")
            ptn["name"] = "PTN Sao Paulo, rho: %s" % str(rho)

            # Perform respective graph calculation and save to file
            target.write(str(rho) + ", " +
                         str(ptn.vcount()) + "," +
                         str(ptn.ecount()) + "," +
                         str(ptn.maxdegree(vertices=None, mode=ALL, loops=True)) + "," +
                         str(ptn.diameter(directed=True)) + "," +
                         str(mean(ptn.degree(mode=ALL, loops=True))) + "," +
                         str(ptn.average_path_length(directed=True)) + "," +
                         str(len(ptn.clusters(mode=WEAK))) + "," +
                         str(ptn.assortativity_degree(directed=True)) + "," +
                         str(ptn.transitivity_undirected()) + "," +
                         str(ptn.density()) + "\n")

            histogram = list(ptn.degree_distribution(bin_width=1, mode="all", loops=True).bins())
            # Save histograms to file for further analysis. File's name with text variable for current rho.
            file4 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histogram/hist%s.txt" % str(rho)
            with open(file4, "w", newline='') as data4:
                data4.write('\n'.join('{},{},{}'.format(x3[0], x3[1], x3[2]) for x3 in histogram))


# Auxiliary function to write results on files for validation with a fixed radius. #run time 6.456102518240611 min
def write_file():

    rho = 30

    file1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/geodata.txt"
    geodata = get_stops_coordinates()
    with open(file1, "w", newline='') as data1:
        for line1 in geodata:
            data1.write("%s\n" % str(line1))

    file2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/neighbors.txt"
    neighbors = get_neighbors(rho, geodata)
    with open(file2, "w", newline='') as data2:
        for line2 in neighbors.items():
            data2.write("%s\n" % str(line2))

    file3 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/grouped.txt"
    grouped = group_stops(neighbors)
    with open(file3, "w", newline='') as data3:
        for line3 in grouped.items():
            data3.write("%s\n" % str(line3))

    file4 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/times.txt"
    times = update_stop_times(grouped)
    with open(file4, "w", newline='') as data4:
        for line4 in times:
            data4.write("%s\n" % str(line4))

    file5 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/validate/edges.txt"
    edges = create_edge_list(times)
    with open(file5, "w", newline='') as data5:
        for line5 in edges:
            data5.write("%s\n" % str(line5))


main()

end = time.time()
elapsed = (end - start) / 60
print(elapsed)
