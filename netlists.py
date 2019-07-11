#!/usr/bin/python


class Pin:
    def __init__(self, component=None, name=""):
        self.component = component
        self.name = name
#        self.component.addPinByName(self.name)

    def __str__(self):
        return str(self.component.designator) + "," + str(self.name)


class Component:
    def __init__(self, designator="", description="", footprint=""):
        self.designator = designator
        self.description = description
        self.footprint = footprint
        self.pins = []

    def findPinByName(self, name):
        for pin in self.pins:
            if pin.name == name:
                return pin
        return None

    def addPinByName(self, name):
        p = self.findPinByName(name)
        if p is None:
            p = Pin(component=self, name=name)
            self.pins += [p]
        return p


class Net:
    def __init__(self, label=""):
        self.label = label
        self.pins = []

    def addPin(self, pin):
        self.pins += [pin]


class Netlist:
    def findComponentByDesignator(self, designator):
        for component in self.components:
            if component.designator == designator:
                return component
        print("Error: Component not found: "+designator)
        return None
