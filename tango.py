#!/usr/bin/python

import re
from netlists import *


class TangoNetlist(Netlist):
    def __init__(self, filename=None):
        if not (filename is None):
            self.read(filename)
            self.parse()

    def read(self, filename):
        f = open(filename, "r")
        self.text = f.read()
        #print(self.text)
        f.close()

    def parse(self):
        # Parse netlist components
        r = re.compile("\[\r\n([^\r]+)\r\n([^\r]*)\r\n([^\r]*)\r\n[^\]]*\]")
        l = re.findall(r, self.text)
        self.components = []
        for result in l:
            designator = result[0]
            footprint = result[1]
            description = result[2]
            self.components += [ Component(designator=designator, description=description, footprint=footprint) ]
            #print("{:s}: {:s} ({:s})".format(designator, description, footprint))

        print("Found {:d} components:".format(len(self.components)))
        print([c.designator for c in self.components])

        # Parse nets
        r = re.compile("\(\r\n([^\r]+)\r\n([^\)]*)\r\n\)")
        l = re.findall(r, self.text)
        self.nets = []
        for result in l:
            netlabel = result[0]
            net = Net(label=netlabel)

            for pin in result[1].split("\r\n"):
                designator = pin.split(",")[0]
                name = pin.split(",")[1]
                component = self.findComponentByDesignator(designator)
                p = component.addPinByName(name)
                net.addPin(p)
                
            self.nets += [net]
            print("Pins on net {:s}: {:s}".format(net.label, str([str(p) for p in net.pins])))
