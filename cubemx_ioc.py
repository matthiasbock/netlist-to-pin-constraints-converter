#!/usr/bin/python3

#
# STMCubeMX configuration file for a microcontroller
#
class IOC:
    #
    # Import the give file
    #
    def __init__(self, filename):
        f = open(filename, "r")
        self.lines = f.read().split("\n")
        f.close()

    #
    # Extract the name of the MCU
    # which is being configured in this file
    #
    def getMcuName(self):
        for line in self.lines:
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            if line.upper().find("MCU.NAME=") > -1:
                name = line.split("=")[1]
                return name
        return None

    #
    # Find and return the pin for which the given
    # alternate function is configured
    #
    def getPinBySignal(self, af, acceptLabelMatch=False):
        AF = af.upper()
        for line in self.lines:
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue

            # A label match has priority over a signal match
            if acceptLabelMatch and (line.upper().find(".GPIO_LABEL=" + AF) > -1):
                pin = line.split(".")[0]
                return pin

            if line.upper().find(".SIGNAL=" + AF) > -1:
                pin = line.split(".")[0]
                return pin
        return None


#
# Test the above class by importing a STMCubeMX configuration file
#
if __name__ == "__main__":
    f = IOC("tests/demo-cubemx-project.ioc")
    print("MCU name: {:s}".format(f.getMcuName()))
    net = "SPI1_NSS"
    print("Function {:s} is configured to: {:s}".format(net, f.getPinByAlternateFunction(net)))
