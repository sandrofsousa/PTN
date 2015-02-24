# def read_file():
#     path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
#     data = open(path, "r")
#     result = data.readline()
#     # get trip_id, stop_id and stop_sequence from line in file
#     for result in data:
#         search_comma = result.split(',')
#         trip_id = search_comma[0]
#         stop_id = search_comma[3]
#         stop_sequence = search_comma[4]
#     return trip_id, int(stop_id), int(stop_sequence)
# print(read_file())


# path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
# data = open(path, "r")
# temp = []
# result = data.readline()
# for result in data:
#     search_comma = result.split(',')
#     trip_id = search_comma[0]
#     stop_id = search_comma[3]
#     stop_sequence = search_comma[4]
#     temp.append([trip_id, int(stop_id), int(stop_sequence)])
# print(temp)


# def read_file():
#     path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
#     with open(path, "r") as data:
#         for line in data:
#             result = data.readline()
#             search_comma = result.split(',')
#             trip_id = search_comma[0]
#             stop_id = search_comma[3]
#             stop_sequence = search_comma[4]
#             print(trip_id, int(stop_id), int(stop_sequence))
#     data.close()
#     print(trip_id, int(stop_id), int(stop_sequence))
#
# print(read_file())


# path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
# tpath = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy 2.txt"
# target = open(tpath, "w")
# data = open(path, "r")
# # temp = []
# result = data.readline()
# for result in data:
#     search_comma = result.split(',')
#     trip_id = str(search_comma[0])
#     stop_id = str(search_comma[3])
#     stop_sequence = str(search_comma[4])
#     target.writelines([trip_id, stop_id, stop_sequence])
# target.close()
# target.writelines(temp)
#
path = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/stop_times copy.txt"
with open(path, "r") as data:
    result_old = data.readline()
    search_comma = result_old.split(',')
    trip_old = search_comma[0]
    stop_old = int(search_comma[3])

    result_new = data.readline()
    search_comma = result_new.split(',')
    trip_new = search_comma[0]
    stop_new = int(search_comma[3])

    edge_list = []

    for line in data:
        if trip_old == trip_new:
            edge_list.append([stop_old, stop_new, trip_old])
            continue

    print(stop_old, stop_new, trip_old)

    #print(stop_old, stop_new, trip_old, trip_new)
    print(edge_list)