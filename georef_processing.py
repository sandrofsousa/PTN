__author__ = 'sandrofsousa'

rsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stopscopy.txt"
wsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stops.txt"

nodes_id = []
nodes_lat = []
nodes_lon = []


def load_nodes_coordinates_from_file(file_name):
    global nodes_id, nodes_lon, nodes_lat
    with open(file_name, "r") as data:
        i = 0
        for line in data:
            if i == 0:
                i += 1
                continue
            line_info = line.strip().split(',')
            nodes_id.append(line_info[0])
            nodes_lat.append(line_info[3])
            nodes_lon.append(line_info[4])
            i += 1
        data.close()
    return nodes_id, nodes_lat, nodes_lon



def nodes_coordinates_distances(lat_list, lon_list):
    global nodes_id, nodes_lon, nodes_lat
    for i in range(len(lat_list)):

# TODO convert coordinates to distance

# TODO compare nodes radios and group

# TODO decide witch node quip when near

