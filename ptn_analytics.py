#
# ----- Public Transport Network of São Paulo as a Complex Network -----
#
# Analysis of GTFS data (Bus, subway adn train system) from SPTrans.
#
# This first approach focus on an empirical analysis of the Network using graph theory,
# calculating degree distribution, centrality, hubs, clusters and another network metrics


read_file = open("/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times.txt", "r")

print(read_file)