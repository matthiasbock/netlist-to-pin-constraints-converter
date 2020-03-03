#!/usr/bin/python3

import sys

#
# Import a CSV as row list of columns
#
# When unspecified, the delimiter is detected automatically.
# Compatible with Linux and Windows linebreaks.
#
def importCSV(filename, delimiter=None):
    f = open(filename, "r")
    data = f.read()
    f.close()
    if delimiter is None:
        # The delimiter was not specified. Attempt to auto-detect it.
        if data.find(";") > -1:
            delimiter = ";"
        elif data.find(",") > -1:
            delimiter = ","
        elif data.find("\t") > -1:
            delimiter = "\t"
        else:
            print("Fatal: Failed to detect delimiter. Unable to import CSV.")
            sys.exit(1)

    # Convert linebreak characters
    data = data.replace("\r\n", "\n").replace("\n\r", "\n").replace("\r", "\n")

    result = []
    for line in data.split("\n"):
        columns = line.split(delimiter)
        result += [columns]
    return result
