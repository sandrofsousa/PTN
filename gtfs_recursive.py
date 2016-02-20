__author__ = 'sandrofsousa'

# Imports
from csv import reader
from math import sin, cos, sqrt, atan2, radians


# Function to read GTFS file and get latitude and longitude from stops.
def get_stops_coordinates():  # PASSED
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stops.txt"
    geodata = []

    with open(file, "r", newline='') as data:
        # parse data using csv based on ',' position.
        searcher = reader(data, delimiter=',', quotechar='"')
        # skip header (first line).
        next(searcher)
        for line in searcher:
            # select the respective column of line based on ',' position.
            stop_id = int(line[0])
            stop_lat = float(line[3])
            stop_lon = float(line[4])

            # append result to the list
            geodata.append((stop_id, stop_lat, stop_lon))

        data.close()
    return geodata


# Function to calculate distance in meters from two latitude and longitude.
def distance_on_sphere(lat1, lon1, lat2, lon2):  # PASSED
    # approximate mean radius of earth in meters
    r = 6371007.176

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dif_lat = lat2 - lat1
    dif_lon = lon2 - lon1

    # Haversine formula to calculate the great-circle distance between two points
    a = sin(dif_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


# Function to process stops file and return the list of nearby stops based on a rho radius vector.
def get_neighbors(radius, stops_list):  # PASSED
    neighbors = dict()

    for row in range(len(stops_list)):
        stop = stops_list[row][0]
        neighbors[stop] = []

    # loop reading the lists of stops, ignoring the last stop.
    for row1 in range(len(stops_list) - 1):
        # Get values from first row.
        stop1 = stops_list[row1][0]
        lat1 = stops_list[row1][1]
        lon1 = stops_list[row1][2]

        # loop reading the lists of stops, skipping the first row.
        for row2 in range(row1 + 1, len(stops_list)):
            # Get values from second row.
            stop2 = stops_list[row2][0]
            lat2 = stops_list[row2][1]
            lon2 = stops_list[row2][2]

            # call function to calculate the distance between two stops coordinates.
            distance = distance_on_sphere(lat1, lon1, lat2, lon2)

            # If distance <= rho, save two stops - they are close each other. Else, keep searchin on file.
            if distance <= radius:
                neighbors[stop1].append(stop2)
            else:
                continue
    return neighbors
# 1,15: [16]

# Recursive function to get neighbors of neighbors and group stops linearly
def recursive_search(series, aux_list, neighbors):
    rec_stop = []
    for stop in aux_list:
        if stop not in series:
            aux_list.remove(stop)
            series.append(stop)
            rec_stop = neighbors[stop]
            aux_list += rec_stop
            recursive_search(series, aux_list, neighbors)
        else:
            aux_list.remove(stop)
    return series


# Function to process neighbors IDs list from previous algorithm and replace them with a new id for grouped stops.
def group_stops(neighbors_dict):
    # Pared lists to store stop id on left and new id on right if there's a neighbor.
    grouped = {}
    last_id = 0
    series = []
    aux_list = []

    # For any item in dict, fill series list with stop to be analysed and aux list with it' neighbors
    for item in neighbors_dict:
        if item in grouped: continue

        series = [item]
        aux_list = neighbors_dict[item]

        # if len(aux_list) == 0:
        #     continue
        # else:
        cluster = recursive_search(series, aux_list, neighbors)

        for stop in cluster:
            grouped[stop] = "v" + str(last_id + 1)
        last_id += 1  # update last_id list to keep consistent sequence

    return grouped


# radius = 30
# stops = get_stops_coordinates()
# neighbors = get_neighbors(radius, stops)

neighbors = {1:[15,16],
             2:[],
             3:[8,12],
             4:[9,11,12],
             5:[11],
             6:[17],
             7:[],
             8:[3],
             9:[4,12],
             10:[11],
             11:[4,5,10],
             12:[3,4,9,13],
             13:[12],
             14:[15],
             15:[1,14],
             16:[1,17],
             17:[6,16]}

grouped = group_stops(neighbors)
print(grouped)
