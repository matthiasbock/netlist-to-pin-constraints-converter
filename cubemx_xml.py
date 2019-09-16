#!/usr/bin/python3

from xml.dom import minidom
import os, sys


#
# Class to allow operations on CubeMX MCU device parameter files
#
class CubeXML:
    def __init__(self, filename, errorsAreFatal=True):
        # Does the file exist?
        if not os.path.exists(filename):
            print("Error: File not found.")
            if errorsAreFatal:
                sys.exit(4)
            return

        # Import XML
        try:
            self.xml = minidom.parse(filename)
        except:
            print("Error: Failed to parse MCU description file.")
            if errorsAreFatal:
                sys.exit(4)
            return

        # Find XML node with MCU configuration
        results = self.xml.getElementsByTagName("Mcu")
        if len(results) < 1:
            print("Error: Root node (\"<Mcu ...\") not found in MCU description file.")
            if errorsAreFatal:
                sys.exit(5)
            return
        self.rootNode = results[0]

        # Extract a list of pins for this MCU
        self.pins = self.rootNode.getElementsByTagName("Pin")

    #
    # Returns the pin number (e.g. 2) of the given pin name (e.g. PC13)
    #
    def getPinNumber(self, pinName):
        # Acceptable argument?
        if pinName == "":
            return None

        # Iterate over all MCU pins
        for pin in self.pins:
            keys = pin.attributes.keys()

            # If the pin's name matches...
            key = "Name"
            if not (key in keys):
                continue
            name = pin.attributes[key].value
            if name != pinName:
                continue

            # ...then extract the pin number
            key = "Position"
            if not (key in keys):
                continue
            position = int(pin.attributes[key].value)
            return position
        return None


#
# Test the above class by importing a STMCubeMX device file
#
if __name__ == "__main__":
    # Test data
    pinName = "PB12"
    expectedPin = 33

    # Test
    f = CubeXML("tests/stm32cubemx/STM32F446R(C-E)Tx.xml")
    pin = f.getPinNumber(pinName)

    # Test result evaluation
    if pin is None:
        print("Test failed: Unable to detect the pin number of {:s}.".format(pinName))
        exit(5)
    if pin != expectedPin:
        print("Test failed: The wrong pin was detected. Got {:d} instead of {:d}.".format(pin, expectedPin))
        exit(5)
    print("Test succeeded: {:s} is located at pin number {:d}.".format(pinName, pin))
