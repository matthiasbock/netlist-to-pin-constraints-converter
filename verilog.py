#!/usr/bin/python3
#
# This file allows for parsing a flattened Verilog module
# as it is generated by Yosys after synthesis
# and for evaluation of simple assertions
#

import re
from netlists import Netlist

#
# A list of submodules accepted as primitives
#
primitives = [
    "SB_LUT4",
    "SB_DFFES",
    "SB_DFFER",
    "SB_PLL40_CORE"
]

#
# Some regular expressions to help us parsing
#
pattern_signal              = "[a-zA-Z0-9\_\\\.\[\:\]]+"
pattern_signal_or_literal   = "[a-zA-Z0-9\_\\\.\[\:\]\']+"
regex_literal_decimal       = re.compile("[0-9]+")
regex_literal_hexadecimal   = re.compile("[0-9]+\'h[0-9a-fA-FxX]+")
regex_literal_binary        = re.compile("[0-9]+\'b[0-1xX]+")
regex_assign                = re.compile("[\t ]*assign[\t ]+(" + pattern_signal + ")[\t ]*=[\t ]*(" + pattern_signal_or_literal + ")[\t ]*;[\t ]*\n")


#
# A class to hold static assertion methods
#
class assertion:
    def isLiteral(expression):
        if regex_literal_decimal.fullmatch(expression) \
        or regex_literal_hexadecimal.fullmatch(expression) \
        or regex_literal_binary.fullmatch(expression):
            return True
        return False

    def netExists(netlist, net):
        assign = netlist.findAssign(net)
        if assign is None:
            print("Net {:s} is not part of the design.".format(net))
            return False
        print("Net {:s} is part of the design.".format(net))
        return True

    def netIsConstant(netlist, net):
        #
        # If it is constant, then there must be
        # a line in the form: assign netname = literal;
        #
        assign = netlist.findAssign(net)

        if assign is None:
            print("Net {:s} is not driven at all.".format(net))
            return True

        if assertion.isLiteral(assign["rhs"]):
            print("Net {:s} is driven by a constant.".format(net))
            return True

        print("Net {:s} is driven by something but not by a constant.".format(net))
        return False

    def netIsNotConstant(netlist, net):
        assign = netlist.findAssign(net)

        if assign is None:
            print("Net {:s} is not driven at all.".format(net))
            return False

        if assertion.isLiteral(assign["rhs"]):
            print("Net {:s} is driven by constant {:s}.".format(net, assign["rhs"]))
            return False

        print("Net {:s} is driven by something but not by a constant.".format(net))
        return True


#
# A class to hold all relevant information about a flattened Verilog file
#
# class File(Netlist):
class File():
    def __init__(self, filename):
        f = open(filename, "r")
        self.content = f.read()
        f.close()
        self.lines = self.content.split("\n")
        self.parseAssigns()

    # Parse all assign statements into an array
    def parseAssigns(self):
        results = re.findall(regex_assign, self.content)
        # print(results)

        self.assigns = []
        for result in results:
            lhs = result[0]
            rhs = result[1]
            # print("{:s} - {:s}".format(lhs, rhs))
            # print("assign {:s} = {:s};".format(lhs, rhs))
            assign = {"lhs": lhs, "rhs": rhs}
            self.assigns += [assign]

    # Find an assign statement for the given netlabel
    def findAssign(self, netlabel):
        netlabel = netlabel.lower()
        for assign in self.assigns:
            if assign["lhs"].lower() == netlabel:
                return assign
        return None


#
# A class to hold a list of assertions a Verilog netlist must fulfill
#
class Assertions():
    def __init__(self):
        self.assertions = []

    def append(self, assertion, arg0=""):
        self.assertions += [[assertion, arg0]]

    def apply(self, netlist):
        for assertion in self.assertions:
            self.applyAssertion(netlist, assertion)

    def applyAssertion(self, netlist, assertion):
        if assertion[0](netlist, assertion[1]):
            print("[SUCCESS] {:s}(\"{:s}\")".format(str(assertion[0]), str(assertion[1])))
        else:
            print("[FAILED]  {:s}(\"{:s}\")".format(str(assertion[0]), str(assertion[1])))