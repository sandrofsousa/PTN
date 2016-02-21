__author__ = 'sandrofsousa'

# Imports
from csv import reader
from math import sin, cos, sqrt, atan2, radians
from igraph import *


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
            else:
                continue
    return neighbors


# Recursive function to get neighbors of respective stop and search for neighbors of each element of the list.
# It return a list with the cluster of neighbors joined linearly.
def recursive_search(series, aux_list, neighbors):
    rec_stop = []

    # For element in the list of neighbors, search for it' own neighbors and increment aux_list.
    for stop in aux_list:
        if stop not in series:
            series.append(stop)
            rec_stop = neighbors[stop]
            aux_list += rec_stop
            return recursive_search(series, aux_list, neighbors)    # Call the function again for each neighbor.
        else:
            continue
    return series


# Function to process neighbors IDs list from previous algorithm and replace them with a new id for grouped stops.
def group_stops(neighbors_dict):
    grouped = {}
    last_id = 0
    series = []
    aux_list = []

    # For each item in neighbors_dict, fill series list with stop to be analysed and aux list with it's neighbors.
    for item in neighbors_dict:
        if item in grouped:                 # Id already parsed, ignore.
            continue

        series = [item]                     # Initialize list with stop to be searched.
        aux_list = neighbors_dict[item]     # Populate list with neighbors of stops

        # Call recursive function to search for neighbors of elements of aux_list
        cluster = recursive_search(series, aux_list, neighbors)

        # Set the same new ID for all elements of the cluster
        for stop in cluster:
            grouped[stop] = "v" + str(last_id + 1)
        last_id += 1    # update last_id list to keep consistent sequence

    return grouped


# Read stop times and replace the current stop on route sequence with new id when it exist from grouped list.
def update_stop_times(grouped_dict):
    file1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stop_times.txt"
    new_stop_times = []

    with open(file1, "r", newline='') as times:
        # parse data using csv based on ',' position.
        searcher = reader(times, delimiter=',', quotechar='"')
        # skip header (first line).
        next(searcher)
        for line in searcher:
            # select the respective column of line based on ',' position and update list serially.
            trip_id = str(line[0])
            stop_id = int(line[3])
            new_stop_times.append((trip_id, str(grouped_dict[stop_id])))

        # close files
        times.close()

    return new_stop_times


# Function to create edge list from stops updated at previous script
def create_edge_list(times_list):
    edge_list = []

    # start index at 0 and finish at last line from list
    for row in range(0, len(times_list) - 1):
        trip1 = times_list[row][0]
        stop1 = times_list[row][1]
        trip2 = times_list[row + 1][0]   # get trip_id from next line
        stop2 = times_list[row + 1][1]   # get stop_id from next line

        # Create link only if stops are in the same line sequence
        if trip1 == trip2:
            edge_list.append((str(stop1), str(stop2), str(trip1)))

    return edge_list


# Main function to process gtfs sub-functions, returns a new edge list and process graph statistics.
def main():
    geodata = get_stops_coordinates()
    radius = list(range(0, 205, 5))
    result = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/radius_0to200.txt"

    with open(result, "w") as target:
        for rho in radius:
            neighbors = get_neighbors(rho, geodata)
            grouped = group_stops(neighbors)
            times = update_stop_times(grouped)
            edges = create_edge_list(times)

            # Save grouped dictionary to file for further verification. File's name with text variable for current rho.
            file1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/grouped/groups%s.txt" %str(rho)
            with open(file1, "w", newline='') as data1:
                data1.write('\n'.join('{},{}'.format(x[0], x[1]) for x in grouped.items()))

            # Save edge lists to file for further verification. File's name with text variable for current rho.
            file2 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edges/edges%s.txt" %str(rho)
            with open(file2, "w", newline='') as data2:
                data2.write('\n'.join('{},{},{}'.format(x[0], x[1], x[2]) for x in edges))

            # Create graph from list of tuples.
            ptn = Graph.TupleList(edges, directed=True, vertex_name_attr="name", edge_attrs="trip")
            ptn["name"] = "PTN Sao Paulo, rho: %s" %str(rho)
            hist = list(ptn.degree_distribution(bin_width=1, mode="all", loops=True).bins())

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

            # Save histograms to file for further analysis. File's name with text variable for current rho.
            file3 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/histograms/hist%s.txt" %str(rho)
            with open(file3, "w", newline='') as data3:
                data3.write('\n'.join('{},{},{}'.format(x[0], x[1], x[2]) for x in hist))


# neighbors = {1:[15,16],
#              2:[],
#              3:[8,12],
#              4:[9,11,12],
#              5:[11],
#              6:[17],
#              7:[],
#              8:[3],
#              9:[4,12],
#              10:[11],
#              11:[4,5,10],
#              12:[3,4,9,13],
#              13:[12],
#              14:[15],
#              15:[1,14],
#              16:[1,17],
#              17:[6,16],
#              18:[],
#              19:[],
#              20:[19]}
