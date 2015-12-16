__author__ = 'sandrofsousa'

# Function to read GTFS file from local directory and save processed result to a new file.
# Data time stamp = 04 Mar. 2015 at 17:47.


def gtfs_to_edge_list():
    rsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/GTFS/stop_times.txt"
    wsource = "/Users/sandrofsousa/Google Drive/Mestrado USP/Dissertação/PTN Data/edge_list.txt"
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
        # close files.
        data.close()
        target.close()

gtfs_to_edge_list()

list1 = [
    ('1018-10-0', 830004082)
    ,('1018-10-0', 830003997)
    ,('1018-10-0', 830003995)
    ,('1018-10-0', 2449)
    ,('1018-10-0', 840000580)
    ,('1018-10-0', 2489)
    ,('1018-10-0', 710000603)
    ,('1018-10-0', 710000604)
    ,('1018-10-0', 710000605)
    ,('1018-10-0', 622)
    ,('1018-10-1', 622)
    ,('1018-10-1', 710017210)
    ,('1018-10-1', 710000974)
    ,('1018-10-1', 710000975)
    ,('1018-10-1', 840000676)
    ,('1018-10-1', 2489)
    ,('1018-10-1', 2449)
    ,('1018-10-1', 830004026)
    ,('1018-10-1', 2454)
    ,('1021-10-0', 4114473)
    ,('1021-10-0', 361)
    ,('1021-10-0', 410003407)
    ,('1021-10-0', 1594)
    ,('1021-10-0', 4114444)
    ,('1021-10-0', 410003413)
    ,('1021-10-0', 2070)
    ,('1021-10-0', 2090)
    ,('1021-10-0', 2090)
    ,('1021-10-0', 2090)
    ,('1021-10-1', 2090)
    ,('1021-10-1', 2090)
    ,('1021-10-1', 2090)
    ,('1021-10-1', 2073)
    ,('1021-10-1', 2074)
    ,('1021-10-1', 2072)
    ,('1021-10-1', 640000377)
    ,('1021-10-1', 640000375)
    ,('1021-10-1', 640000489)
    ,('1021-10-1', 410003416)
    ,('1021-10-1', 361)
    ,('1024-10-0', 928)
    ,('1024-10-0', 928)
    ,('1024-10-0', 929)
    ,('1024-10-0', 930)
    ,('1024-10-0', 1114034)
    ,('1024-10-0', 1321)
    ,('1024-10-0', 290001365)
    ,('1024-10-0', 290001363)
    ,('1024-10-0', 290001362)
    ,('1024-10-0', 208)
    ,('1024-10-1', 208)
    ,('1024-10-1', 290001361)
    ,('1024-10-1', 290001364)
    ,('1024-10-1', 2914536)
    ,('1024-10-1', 930)
    ,('1024-10-1', 929)
    ,('1024-10-1', 928)
    ,('1024-10-1', 928)
    ,('1025-10-0', 1114267)
    ,('1025-10-0', 110003357)
    ,('1025-10-0', 931)
    ,('1025-10-0', 930)
    ,('1025-10-0', 1114034)
    ,('1025-10-0', 1321)
    ,('1025-10-0', 290001365)
    ,('1025-10-0', 290001363)
    ,('1025-10-0', 290001362)
    ,('1025-10-0', 208)
    ,('1025-10-1', 208)
    ,('1025-10-1', 290001361)
    ,('1025-10-1', 290001364)
    ,('1025-10-1', 2914536)
    ,('1025-10-1', 930)
    ,('1025-10-1', 931)
    ,('1025-10-1', 1114267)]