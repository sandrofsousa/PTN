__author__ = 'sandrofsousa'

from csv import reader
from math import sin, cos, sqrt, atan2, radians


# Function to read GTFS file and get latitude and longitude from stops.
def get_stops_geodata():
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stops_sample.txt" # TODO change to full

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
    R = 6371000.0

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dif_lat = lat2 - lat1
    dif_lon = lon2 - lon1

    # Haversine formula to calculate the great-circle distance between two points
    a = sin(dif_lat / 2)**2 + cos(lat1) * cos(lat2) * sin(dif_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c

    return distance


# Algorithm 1 to process GTFS file and return the list of stops in a proximity based on a rho vector.
def algorithm_1(rho):
    stops = []
    data = get_stops_geodata()

    # loop reading the lists of stops, ignoring the last stop.
    for row1 in range(len(data) - 1):
        # Get values from first row.
        stop1 = data[row1][0]
        lat1 = data[row1][1]
        lon1 = data[row1][2]

        # loop reading the lists of stops, skipping the first row.
        for row2 in range(row1 + 1, len(data)):
            # Get values from second row.
            stop2 = data[row2][0]
            lat2 = data[row2][1]
            lon2 = data[row2][2]

            # call function to calculate the distance between two stops coordinates.
            distance = calc_stops_distance(lat1, lon1, lat2, lon2)

            # If distance <= rho, save two stops - they are close each other. Else, keep searchin on file.
            if distance <= rho:
                stops.append((stop1, stop2))
            else:
                continue
    return stops
# TODO save results to file


############################################################################################


# Algorithm 2 to process grouped IDs list from previous algorithm and replace them with a new id for the grouped stops.
def algorithm_2():
