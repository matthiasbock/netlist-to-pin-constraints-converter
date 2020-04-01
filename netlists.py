#!/usr/bin/python


#
# A pin is one physical connection of a component.
# It has a name (string) and a reference to it's component (object reference).
#
class Pin:
    def __init__(self, component=None, name=""):
        self.component = component
        self.name = name

    def getName(self):
        return self.name

    def getComponent(self):
        return self.component

    def __str__(self):
        return self.getComponent().getDesignator() + "," + self.getName()


#
# Electrical component, as found on a PCB
# has a designator (string) and a list of pins,
# maybe also a description (string) and a footprint (string)
#
class Component:
    def __init__(self, designator="", description="", footprint=""):
        self.designator = designator.strip()
        if self.designator == "*":
            print("Warning: Created component with wildcard designator.")
        self.description = description.strip()
        self.footprint = footprint.strip()
        self.pins = []

    def getPinByNumber(self, number):
        if len(self.pins) < number:
            return None
        return self.pins[number-1]

    def getPinByName(self, name):
        for pin in self.pins:
            if str(pin.getName()) == str(name):
                return pin
        return None

    def createPinFromName(self, name):
        # Does a pin with that name already exist?
        p = self.getPinByName(name)
        if p is None:
            p = Pin(component=self, name=name)
            self.pins += [p]
        return p

    def getDesignator(self):
        return self.designator

    def getDescription(self):
        return self.description

    def getPins(self):
        return self.pins


#
# A net is a list of connected pins.
# It has a name i.e. label and a list of pins (object references).
#
class Net:
    def __init__(self, label=""):
        self.label = label
        self.pins = []

    def getLabel(self):
        return self.label

    def isPower(self):
        # TODO: Match regexp to detect power net label
        return self.label in ["GND", "DGND", "1V2", "1.2V", "3V3", "3.3V", "5V", "12V", "HV+", "HV-", "DC+", "DC-"]

    def addPin(self, pin):
        self.pins += [pin]

    def getPins(self):
        return self.pins

    #
    # Return the first pin on this net, which belongs
    # to a component with the given designator
    #
    def getPin(self, componentDesignator=None):
        if componentDesignator is None:
            return None
        componentDesignator = componentDesignator.upper().strip()
        for pin in self.pins:
            if pin.getComponent().getDesignator().upper() == componentDesignator:
                return pin
        return None

    def __str__(self):
        return self.getLabel()


#
# Convert string for compatibility with regular expressions
#
def cleanupEncoding(s):
    return str(s.encode("ascii", "replace")).replace("\\n", "\n")


#
# A list of components and nets
# (both stored as a object references).
#
class Netlist:
    def __init__(self):
        self.components = []
        self.nets = []

    #
    # Only reads the text from a file.
    # A format-specific method still needs
    # to take care of parsing afterwards.
    #
    def readFromFile(self, filename):
        f = open(filename, "r", encoding="iso8859_15")
        # f = open(filename, "r")
        self.text = cleanupEncoding(f.read())
        # print(self.text)
        f.close()

    #
    # Return all components in this netlist
    #
    def getComponents(self):
        return self.components

    #
    # Return all nets in this netlist
    #
    def getNets(self):
        return self.nets

    #
    # Returns the net with the given label if present, else None
    #
    def getNet(self, netlabel):
        for net in self.getNets():
            if net.getLabel() == netlabel:
                return net
        return None

    #
    # Returns true, if the given net is present in this netlist
    #
    def hasNet(self, netlabel):
        return not (self.getNet(netlabel) is None)

    #
    # Return the component with the given designator (not case-sensitive)
    #
    def getComponentByDesignator(self, designator):
        designator = designator.upper().strip()
        for component in self.components:
            if component.getDesignator().upper() == designator:
                return component
        print("Error: Component not found: " + designator)
        return None

    #
    # Return the component with the given description (not case-sensitive)
    #
    def getComponentByDescription(self, description):
        description = description.upper().strip()
        for component in self.components:
            if component.getDescription().upper() == description:
                return component
        print("Error: Component not found: " + description)
        return None

    #
    # Return the first component containing the given keyword
    # in either description or designator (not case-sensitive)
    #
    def getComponentByKeyword(self, keyword):
        keyword = keyword.upper().strip()
        component = None
        for component in self.getComponents():
            if (component.getDesignator().upper().find(keyword) > -1) \
            or (component.getDescription().upper().find(keyword) > -1):
                return component
        print("Error: Component not found.")
        return None

    #
    # A convenience wrapper for the above methods
    #
    def getComponent(self, designator=None, description=None, keyword=None):
        if not (designator is None):
            return self.getComponentByDesignator(designator)
        if not (description is None):
            return self.getComponentByDescription(description)
        if not (keyword is None):
            return self.getComponentByKeyword(keyword)
        return None

    #
    # Returns the net (object reference) of the given pin (object reference)
    #
    def getNetOnPin(self, pin, debug=False):
        if pin is None:
            if debug:
                print("Error: Illegal argument None given to getNetOnPin().")
            return None
        for net in self.getNets():
            for p in net.getPins():
                if p == pin:
                    if debug:
                        print("Found net {:s} for component {:s}, pin {:s}.".format(net.getLabel(), p.getComponent().getDesignator(), p.getName()))
                    return net
        if debug:
            print("Error: Unable to detect the net connected to component {:s}, pin {:s}.".format(pin.getComponent().getDesignator(), pin.getName()))
        return None

    #
    # Extract all connections between two components (except power pins)
    # Requires the two components' designators and
    # returns a list of Net objects
    #
    def elaborateComponentConnections(self, designator1, designator2, debug=False):
        #
        # Iterate over all netlist nets and extract the ones with pins matching the given designators
        #
        connectedNets = []
        for net in self.getNets():
            pin1 = net.getPin(componentDesignator=designator1)
            if pin1 is None:
                # Component 1 is not connected to this net
                continue

            pin2 = net.getPin(componentDesignator=designator2)
            if pin2 is None:
                # Component 2 is not connected to this net
                continue

            if net.isPower():
                # Disregard non-signal net
                print("Info: Net {:s} is a power net. Skipping.".format(net.getLabel()))
                continue

            if len(net.getPins()) < 2:
                # Disregard unconnected nets
                print("Info: Net {:s} is not connected anywhere. Skipping.".format(net.getLabel()))
                continue

            if debug:
                print("Component {:s} pin {:s} is connected to component {:s} pin {:s} on net {:s}." \
                      .format(
                          designator1,
                          pin1.getName(),
                          designator2,
                          pin2.getName(),
                          net.getLabel()
                          )
                      )
            connectedNets += [(net, pin1, pin2)]

        return connectedNets
