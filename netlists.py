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
        return str(self.component.designator) + "," + str(self.name)


#
# Electrical component, as found on a PCB
# has a designator (string) and a list of pins,
# maybe also a description (string) and a footprint (string)
#
class Component:
    def __init__(self, designator="", description="", footprint=""):
        self.designator = designator.strip()
        self.description = description.strip()
        self.footprint = footprint.strip()
        self.pins = []

    def findPinByName(self, name):
        for pin in self.pins:
            if pin.name == name:
                return pin
        return None

    def addPinByName(self, name):
        # Does a pin with that name already exist?
        p = self.findPinByName(name)
        if p is None:
            p = Pin(component=self.getDesignator(), name=name)
            self.pins += [p]
        return p

    def getDesignator(self):
        return self.designator

    def getDescription(self):
        return self.description


#
# A net is a list of connected pins.
# It has a name i.e. label.
#
class Net:
    def __init__(self, label=""):
        self.label = label
        self.pins = []

    def getLabel(self):
        return self.label

    def isPower(self):
        # TODO: Match regexp to detect power net label
        return self.label in ["GND", "1V2", "1.2V", "3V3", "3.3V", "5V", "12V"]

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

#
# A list of components and nets
#
class Netlist:
    def __init__(self):
        self.components = []
        self.nets = []

    def findComponentByDesignator(self, designator):
        designator = designator.upper().strip()
        for component in self.components:
            if component.getDesignator().upper() == designator:
                return component
        print("Error: Component not found: " + designator)
        return None

    def findComponentByDescription(self, description):
        description = description.upper().strip()
        for component in self.components:
            if component.getDescription().upper() == description:
                return component
        print("Error: Component not found: " + description)
        return None

    def getComponents(self):
        return self.components

    def getNets(self):
        return self.nets
