#!/usr/bin/python

import re
from netlists import *


#
# Parses and handles a netlist in Tango format
#
class TangoNetlist(Netlist):
    def __init__(self, filename=None, debug=False):
        if not (filename is None):
            self.readFromFile(filename)
            self.parse(debug)

    #
    # Parse the imported text and generate a
    # list of components and nets
    #
    def parse(self, debug=False):
        # Use regular expression to parse components
        r = re.compile("\[\r\n([^\r]+)\r\n([^\r]*)\r\n([^\r]*)\r\n[^\]]*\]")
        l = re.findall(r, self.text)
        self.components = []
        for result in l:
            designator = result[0]
            footprint = result[1]
            description = result[2]
            self.components += [ Component(designator=designator, description=description, footprint=footprint) ]
            if debug:
                print("{:s}: {:s} ({:s})".format(designator, description, footprint))

        if debug:
            print("Found {:d} components:".format(len(self.components)))
            print([c.getDesignator() for c in self.components])

        # Use regular expression to parse nets
        r = re.compile("\(\r\n([^\r]+)\r\n([^\)]*)\r\n\)")
        l = re.findall(r, self.text)
        self.nets = []
        for result in l:
            netlabel = result[0]
            net = Net(label=netlabel)

            for pin in result[1].split("\r\n"):
                designator = pin.split(",")[0]
                name = pin.split(",")[1]
                component = self.getComponent(designator=designator)
                if component is None:
                    print("Error: Net '{:s}' references unknown component '{:s}'. Skipping.".format(netlabel, designator))
                    continue
                p = component.createPinFromName(name)
                net.addPin(p)

            self.nets += [net]
            if debug:
                print("{:d} pin(s) are connected to net '{:s}': {:s}".format(len(net.getPins()), net.getLabel(), str([str(p) for p in net.getPins()])))

