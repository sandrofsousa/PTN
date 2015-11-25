
from csv import reader
from math import sin, cos, sqrt, atan2, radians

__author__ = 'sandrofsousa'


# Function to read GTFS file and get latitude and longitude from stops.
def get_stops_geodata():        # TODO change to full file
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stops_sample.txt"

    # temporary list to store data
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
def calc_stops_distance(lat1, lon1, lat2, lon2):
    # approximate mean radius of earth in meters
    r = 6371000.0

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dif_lat = lat2 - lat1
    dif_lon = lon2 - lon1

    # Haversine formula to calculate the great-circle distance between two points
    a = sin(dif_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = r * c

    return distance


# Algorithm 1 to process stops file and return the list of nearby stops based on a rho radius vector.
def algorithm_1(rho, stops):
    neighbors = []

    # loop reading the lists of stops, ignoring the last stop.
    for row1 in range(len(stops) - 1):
        # Get values from first row.
        stop1 = stops[row1][0]
        lat1 = stops[row1][1]
        lon1 = stops[row1][2]

        # loop reading the lists of stops, skipping the first row.
        for row2 in range(row1 + 1, len(stops)):
            # Get values from second row.
            stop2 = stops[row2][0]
            lat2 = stops[row2][1]
            lon2 = stops[row2][2]

            # call function to calculate the distance between two stops coordinates.
            distance = calc_stops_distance(lat1, lon1, lat2, lon2)

            # If distance <= rho, save two stops - they are close each other. Else, keep searchin on file.
            if distance <= rho:
                neighbors.append((stop1, stop2))
            else:
                continue

    return neighbors


############################################################################################


# Algorithm 2 to process neighbors IDs list from previous algorithm and replace them with a new id for grouped stops.
def algorithm_2(stops, neighbors):
    # Pared lists to store stop id on left and new id on right if there's a neighbor.
    grouped_left = []
    grouped_right = []
    last_id = 0

    # Populate left list with all stops, taking first position of tuple. Right list filled with 0 to keep sync.
    for row in stops:
        stop = row[0]
        grouped_left.append(stop)
        grouped_right.append(0)

    # Get nearby stops from neighbors list.
    for row in neighbors:
        stop1 = row[0]
        stop2 = row[1]

        # Linear search at neighbors list to create an index for both stops.
        stop1_index = grouped_left.index(stop1)
        stop2_index = grouped_left.index(stop2)

        # Position in grouped_right list based on first value of neighbors based on stop1_index.
        # For the case when stop1 is empty: check stop2, if it's also empty - set an equal new ID for both.
        # If stop2 already has a new ID, set the same new ID for stop1.
        if grouped_right[stop1_index] == 0:
            if grouped_right[stop2_index] == 0:
                grouped_right[stop1_index] = last_id + 1
                grouped_right[stop2_index] = last_id + 1
                last_id += 1    # update last_id list to keep consistent sequence
            else:
                grouped_right[stop1_index] = grouped_right[stop2_index]

        # For the case when stop1 has already a new ID: check stop2.
        # If stop2 also empty - set the same new ID from stop1. Otherwise, continue.
        else:
            if grouped_right[stop2_index] == 0:
                grouped_right[stop2_index] = grouped_right[stop1_index]
            else:
                continue

    # Update stops not in neighbors list, replacing zero values in grouped_right with the original stop ID.
    for line in stops:
        stop = line[0]
        stop_index = grouped_left.index(stop)

        # If stop from index equals zero, update grouped_right with index value. Otherwise, continue.
        if grouped_right[stop_index] == 0:
            grouped_right[stop_index] = grouped_left[stop_index]
        else:
            continue

    # Join the two list in only one and split the lines
    return list(zip(grouped_left, grouped_right))


############################################################################################


# Read stop times and replace the current stop on sequence with new id when it exist.
def update_stop_times(grouped):
    file1 = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stop_times.txt"
    trip_times = []
    stop_times = []
    new_stop_times = []

    with open(file1, "r", newline='') as times:
        # parse data using csv based on ',' position.
        searcher = reader(times, delimiter=',', quotechar='"')
        # skip header (first line).
        next(searcher)
        for line in searcher:
            # select the respective column of line based on ',' position and update trip/stop lists.
            trip_id = str(line[0])
            stop_id = int(line[3])
            trip_times.append(trip_id)
            stop_times.append(stop_id)

        times.close()
    # Loop at grouped list
    for row in grouped:
        # select the respective column of line based on ',' position.
        stop1 = row[0]
        stop2 = row[1]
        index = stop_times.index(stop1)

        # If stop1 equals stop2 in grouped list (no new id was given) append trip from index and stop2 IDs.
        if stop1 == stop2:
            new_stop_times.append((trip_times[index], stop2))

        # Otherwise, append trip from index position and stop2 IDs to new_stop_times list.
        else:
            new_stop_times.append((trip_times[index], stop2))

    return new_stop_times


############################################################################################


def main():
    stops = get_stops_geodata()
    rho = 30         # TODO change rho to a vector.
    neighbors = algorithm_1(rho, stops)
    grouped = algorithm_2(stops, neighbors)
    edge_list = update_stop_times(grouped)

    return neighbors, grouped, edge_list
