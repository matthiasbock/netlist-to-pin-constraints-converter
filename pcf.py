#!/usr/bin/python3


#
# Handles generation of a pin constraints file
# for Lattice FPGA projects (.pcf)
#
class PCF:
    def __init__(self):
        self.constraints = []

    def addConstraint(self, signal, pin):
        self.constraints += [[pin, signal]]

    def __str__(self):
        result = "\n"
        for c in self.constraints:
            result += "set_io {:s} {:s}\n".format(c[1], c[0])
        result += "\n"
        return result

    def saveToFile(self, filename):
        f = open(filename, "w")
        f.write(str(self))
        f.close()
