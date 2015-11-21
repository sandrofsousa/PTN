__author__ = 'sandrofsousa'

# Function to read GTFS file and group the stops near each other by a rho radius.
import csv
source_file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stops.txt"


def get_stops_geodata(file_from):
    result = []
    with open(file_from, "r", newline='') as data:
        reader = csv.reader(data, delimiter=',', quotechar='"')
        next(reader)                    # skip header
        for line in reader:             # loop at line
            stop_id = line[0]           # select the first column from line (position 0)
            stop_lat = line[3]          # select the fourth column from line (position 3)
            stop_lon = line[4]          # select the fifth column from line (position 4)
            result.append((stop_id, stop_lat, stop_lon))    #fill result list

        data.close()
    return result
get_stops_geodata(source_file)


def calc_distance_stops(list):




