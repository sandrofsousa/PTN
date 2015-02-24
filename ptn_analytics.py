##########################################################################################################
##                                                                                                      ##
## --------------------------- Public Transport Complex Network of São Paulo -------------------------- ##
##                                                                                                      ##
## Empirical Analysis of GTFS data of São Paulo Public transport network (Bus, subway adn train systems)##
## from SPTrans. The bus stops and subway stations are set as vertex (nodes) and lines/routes as edges  ##
## (links) of the network.                                                                              ##
## Statistical analysis of the Network using graph theory,calculating degree distribution,              ##
## centrality, hubs, clusters and other network metrics.                                                ##
##                                                                                                      ##
## Sousa, Sandro                                                                                        ##
## Complex Systems Modeling                                                                             ##
## University of São Paulo                                                                              ##
## sandrofsousa@gmail.com                                                                               ##
## sandrofs@usp.br                                                                                      ##
##                                                                                                      ##
##########################################################################################################


# Read GTFS file from local directory
path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
with open(path, "r") as data:
    # create two equal lists containing file' lines
    file1 = file2 = [line.strip() for line in data]

    # create an empty list to hold result from loop
    edge_list = []

    # loop reading the two lists created, where the second list is read from the second line
    for line1, line2 in zip(file1, file2[1:]):

        # select the first column from line 1 and 2 (position 0)
        trip_old = line1.split(',')[0]
        trip_new = line2.split(',')[0]

        # select the fourth column from line 1 and 2 (position 3)
        stop_old = line1.split(',')[3]
        stop_new = line2.split(',')[3]

        # Compare if trip_id of line 1 is equal to trip_id of line 2
        if trip_old == trip_new:

            # if true, insert stop_id from line 1 and 2 to edge_list. Trip_id is preserved for edge label.
            edge_list.append([stop_old, stop_new, trip_old])
            continue
    # print list of edges
    print(edge_list)