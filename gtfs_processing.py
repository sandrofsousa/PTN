__author__ = 'sandrofsousa'

from csv import reader
from math import sin, cos, sqrt, atan2, radians


# Function to read GTFS file and get latitude and longitude from stops.
def get_stops_geodata():
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stops.txt"

    # temporary list to store data
    result = []
    with open(file, "r", newline='') as data:

        # parse data using csv based on ',' position.
        searcher = reader(data, delimiter=',', quotechar='"')
        # skip header (first line).
        next(searcher)
        for line in searcher:

            # select the respective column of line based on ',' position.
            stop_id = line[0]
            stop_lat = line[3]
            stop_lon = line[4]
            # append result to the list
            result.append((stop_id, stop_lat, stop_lon))

        data.close()
    return result
# get_stops_geodata()


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

    print(distance)
# calc_stops_distance(lat1, lon1, lat2, lon2)


lat1 = (-23.554190)
lon1 = (-46.670723)
lat2 = (-23.554190)
lon2 = (-46.672000)


def main():
    data = get_stops_geodata()
    rho = 30
    # loop
    for line in data:

        # select the first column from line 1 and 2 (position 0).
        trip_old = line1.split(',')[0]
        trip_new = line2.split(',')[0]

        # select the fourth column from line 1 and 2 (position 3).
        stop_old = line1.split(',')[3]
        stop_new = line2.split(',')[3]