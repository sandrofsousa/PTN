# Function to read GTFS file from local directory and save processed result to a new file.
# Data time stamp = 04 Mar. 2015 at 17:47.

def gtfs_to_edge_list():
    rsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/gtfs/stop_times.txt"
    wsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edge_list_old.txt"
    with open(rsource, "r") as data, open(wsource, "w") as target:
        # create two equal lists containing file' lines
        file1 = file2 = [line.strip() for line in data]
        # loop reading the two lists created, where the second list is read from the second line.
        for line1, line2 in zip(file1, file2[1:]):

            # select the first column from line 1 and 2 (position 0).
            trip_old = line1.split(',')[0]
            trip_new = line2.split(',')[0]

            # select the fourth column from line 1 and 2 (position 3).
            stop_old = line1.split(',')[3]
            stop_new = line2.split(',')[3]

            # Compare if trip_id of line 1 is equal to trip_id of line 2.
            if trip_old == trip_new:

                # if true, write stop_id from line 1 and 2 to target file. Trip_id is preserved as edge label.
                target.writelines([stop_old + ',', stop_new + '\n'])
                continue
