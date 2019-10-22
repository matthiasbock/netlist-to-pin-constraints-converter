#!/usr/bin/python3
#
# This file allows for import and manipulation
# of a pin constraints file
# as it is used in Lattice FPGA projects
#


def cmpPin(a, b):
    return cmp(a[0], b[0])


def cmpSignal(a, b):
    return cmp(a[1], b[1])


#
# Handles generation of a pin constraints file
# for Lattice FPGA projects (.pcf)
#
class PCF:
    def __init__(self):
        self.constraints = []

    def addConstraint(self, signal, pin):
        self.constraints += [[pin, signal]]

    def sortBySignal(self):
        self.constraints = sorted(self.constraints, key = lambda c: c[1])

    def sortByPin(a, b):
        self.constraints = sorted(self.constraints, key = lambda c: c[0])

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
