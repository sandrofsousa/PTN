__author__ = 'sandrofsousa'

from csv import reader
import numpy as np
from collections import OrderedDict


# Function to read GTFS file and get latitude and longitude from stops.
def get_stops_coordinates():  # PASSED
    file = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stops.txt"
    coordinates = {}

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
            coordinates[stop_id] = [stop_lat, stop_lon]

        data.close()
    return coordinates


def distance_on_sphere(coordinates_array):
    # Compute a distance matrix of the coordinates using a spherical metric.
    # :param coordinate_array: numpy.ndarray with shape (n,2); latitude is in 1st col, longitude in 2nd.
    # :returns distance_mat: numpy.ndarray with shape (n, n) containing distance in km between coords.

    # Radius of the earth in km (GRS 80-Ellipsoid)
    EARTH_RADIUS = 6371.007176

    # Unpacking coordinates
    latitudes = coordinates_array[:, 0]
    longitudes = coordinates_array[:, 1]
    n_pts = coordinates_array.shape[0]

    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = np.pi / 180.0
    phi_values = (90.0 - latitudes) * degrees_to_radians
    theta_values = longitudes * degrees_to_radians

    # Expand phi_values and theta_values into grids
    theta_1, theta_2 = np.meshgrid(theta_values, theta_values)
    theta_diff_mat = theta_1 - theta_2

    phi_1, phi_2 = np.meshgrid(phi_values, phi_values)

    # Compute spherical distance from spherical coordinates
    angle = (np.sin(phi_1) * np.sin(phi_2) * np.cos(theta_diff_mat) + np.cos(phi_1) * np.cos(phi_2))
    arc = np.arccos(angle)

    # Multiply by earth's radius to obtain distance in km
    return arc * EARTH_RADIUS


def compute_distance_matrix(coordinates_dict):
    distance_dict = {}

    for stop in coordinates_dict.keys():
        distance_dict[stop] = OrderedDict()
        coord1 = coordinates_dict[stop]

        for other_stop in coordinates_dict.keys():
            coord2 = coordinates_dict[other_stop]
            distance = distance_on_sphere(coord1, coord2)
            distance_dict[stop][other_stop] = distance

    return distance_dict


coordinates_dict = get_stops_coordinates()
coordinates_array = np.array([(val[0], val[1]) for key, val in coordinates_dict.items()])
matrix = distance_on_sphere(coordinates_array)
