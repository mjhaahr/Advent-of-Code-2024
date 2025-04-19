import sys
import os
import re
from itertools import combinations
from copy import deepcopy

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

opPattern = re.compile(r"(.{3}) (AND|OR|XOR) (.{3}) -> (.{3})")

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    values = {}
    ops = []
    maxZ = 0

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        # Parse starting values
        parseVals = True
        for line in fp.readlines():
            line = line.strip()
            if line == "":
                parseVals = False
                continue

            if parseVals:
                var = line[0:3]
                values[var] = int(line[5])
            else:
                m = opPattern.match(line)
                if m:
                    if m.group(4)[0] == 'z':
                        offset = int(m.group(4)[1:3])
                        maxZ = max(offset, maxZ)
                    ops.append(Op(m.group(1), m.group(3), m.group(4), m.group(2)))

    if not part2:
        # Run all operations
        idx = 0
        # Duplicated because of manipulation
        while ops:
            op = ops[idx]
            if op.a in values and op.b in values:
                values[op.out] = op.run(values[op.a], values[op.b])
                del ops[idx]

                if idx >= len(ops):
                    idx = len(ops) - 1
            else:
                idx = (idx + 1) % len(ops)

        # Find All Input and Output Values and assign them
        z = 0
        # Loop over all
        for out, val in values.items():
            if out[0] == 'z':
                offset = int(out[1:3])
                z += val << offset
    else:
        # Part two finds the "swapped" operations
        if "example" in filename:
            swapped = 1
        else:
            swapped = 4

        swaps = []

        # Solve First Adder
        addOp = None
        carryOp = None
        cOut = None
        for op in ops:
            if 'x00' in op.args and 'y00' in op.args:
                if op.op == 'XOR':
                    addOp = op
                elif op.op == 'AND':
                    carryOp = op
                    cOut = op.out


            if addOp is not None and carryOp is not None:
                break

        debug = False
        if debug: print(f"Add {addOp}\nCarry {carryOp}\n")

        # EVAL First Op
        # Remove the ops from savedOps for time savings on later search
        adder = [addOp, carryOp]
        for op in adder:
            ops.remove(op)

        for idx in range(1, maxZ):
            good, adder = evalRipple(cOut, idx, ops, debug)
            if debug: print(good, adder)
            # Remove the ops from savedOps for time savings on later search
            if good:
                cOut = adder[-1].out
                for op in adder:
                    ops.remove(op)
            else:
                # Only occurs within the swap, rather than outside of it
                newSwaps, adder, cOut = findSwap(idx, cOut, ops, debug)
                swaps.extend(newSwaps)
                # Remove the ops from savedOps for time savings on later search
                for op in adder:
                    ops.remove(op)

                if len(swaps) // 2 >= swapped:
                    break

        # Last cOut should be z[maxZ]
        score = ','.join(sorted(swaps))

    # Return Accumulator
    print(score)

# Returns the swapped outputs and the list of operations in the adder stage
# Also needs to return carry out
def findSwap(idx, cIn, ops, debug=False):
    # Steps:
        # Find all operations for the given input
        # Find all the outputs of those operations
        # Find all pairs of those operations and swap their outputs (do it on copies)

    halfAdd = None  # x[idx] ^ y[idx] = halfAdd
    fullAdd = None  # halfAdd ^ cIn = z[idx]

    halfCarry = None # x[idx] & y[idx] = halfCarry
    factorIn = None # halfAdd & cIn = factorIn
    fullCarry = None # halfCarry | factorIn = carryOut

    # Find the operations
    x = f"x{idx:02d}"
    y = f"y{idx:02d}"
    z = f"z{idx:02d}"

    swaps = []
    adder = []

    outputs = set()

    # Find the known ops
    for op in ops:
        if halfAdd is not None and halfCarry is not None:
            break
        if x in op.args and y in op.args:
            if op.op == 'XOR':
                halfAdd = op
                outputs.add(op.out)
                if debug: print("found Half Add")
            elif op.op == 'AND':
                halfCarry = op
                outputs.add(op.out)
                if debug: print("found Half Carry")

    # Find ops with carry in
    for op in ops:
        if fullAdd is not None and factorIn is not None:
            break
        if cIn in op.args:
            if op.op == 'XOR':
                fullAdd = op
                outputs.add(op.out)
                if debug: print("found Full Add")
            elif op.op == 'AND':
                factorIn = op
                outputs.add(op.out)
                if debug: print("found Factor In")

    # Find Full Carry (which will be an OR and one of the inputs will be in the seen outputs)
    for op in ops:
        if op.op == 'OR':
            if op.args.intersection(outputs):
                fullCarry = op
                break

    if debug:
        print(f"Half Adder {halfAdd}")
        print(f"Full Adder {fullAdd}")
        print(f"Half Carry {halfCarry}")
        print(f"Factor In  {factorIn}")
        print(f"Full Carry {fullCarry}")

    # Found all the operations
    adder = [halfAdd, fullAdd, halfCarry, factorIn, fullCarry]

    # How to evaluate swaps?
    for i, j in combinations(range(5), 2):
        newAdder = deepcopy(adder)
        if debug: print(f"Swapping: {adder[i].out} and {adder[j].out}")
        newAdder[i].out = adder[j].out
        newAdder[j].out = adder[i].out

        if checkAdder(newAdder, z, debug):
            swaps = [adder[i].out, adder[j].out]
            # Also get the carry out
            return swaps, adder, newAdder[-1].out

    return [], [], ''


# Returns true if the supplied adder is good
# Adder order is expected: Half Add, Full Add, Half Carry, Factor In, Full Carry
def checkAdder(adder, output, debug):
    # Ways to check adder:
        # Full Add Output is the expected value
        # Half Add Output in Args of Full Add
        # Half Add Output in Args of Factor In
        # Full Carry inputs are Factor In and Half Carry
    halfAdd, fullAdd, halfCarry, factorIn, fullCarry = adder

    # Expected output is wrong
    if fullAdd.out != output:
        if debug: print("  Wrong Output")
        return False

    if halfAdd.out not in fullAdd.args:
        if debug: print("  Half Add not in Full Add")
        return False

    if halfAdd.out not in factorIn.args:
        if debug: print("  Half Add not in Factor In")
        return False

    if set([halfCarry.out, factorIn.out]) != fullCarry.args:
        if debug: print("  Full Carry Inputs are not Factor In and Half Carry")
        return False

    if debug: print("  Good Swap")
    return True



# Returns if the adder is good and the operations to create the full adder (if good)
# If the Order: Half Add, Full Add, Half Carry, Factor In, Full Carry
def evalRipple(cIn, idx, ops, debug=False):
    halfAdd = None  # x[idx] ^ y[idx] = halfAdd
    fullAdd = None  # halfAdd ^ cIn = z[idx]

    halfCarry = None # x[idx] & y[idx] = halfCarry
    factorIn = None # halfAdd & cIn = factorIn
    fullCarry = None # halfCarry | factorIn = carryOut

    # Find the operations
    x = f"x{idx:02d}"
    y = f"y{idx:02d}"

    try:
        for op in ops:
            if halfAdd is not None and halfCarry is not None:
                break
            if x in op.args and y in op.args:
                if op.op == 'XOR':
                    halfAdd = op
                    if debug: print("found Half Add")
                elif op.op == 'AND':
                    halfCarry = op
                    if debug: print("found Half Carry")

        for op in ops:
            if fullAdd is not None and factorIn is not None:
                break
            if halfAdd.out in op.args and cIn in op.args:
                if op.op == 'XOR':
                    fullAdd = op
                    if debug: print("found Full Add")
                elif op.op == 'AND':
                    factorIn = op
                    if debug: print("found Factor In")

        for op in ops:
            if factorIn.out in op.args and halfCarry.out in op.args:
                if op.op == 'OR':
                    fullCarry = op
                    if debug: print("found Full Carry")
                    break

        if fullAdd.out == f"z{idx:02d}":
            #print(f"Half Add {halfAdd}\nFull Add {fullAdd}\nHalf Carry {halfCarry}\nFactor In {factorIn}\nFull Carry {fullCarry}\n")
            return True, [halfAdd, fullAdd, halfCarry, factorIn, fullCarry]


    except AttributeError:
        pass

    return False, []


class Op:
    def __init__(self, a, b, out, op):
        self.a = a
        self.b = b
        self.out = out
        self.op = op
        self.ran = False
        self.args = set([self.a, self.b])

    def run(self, a, b):
        self.ran = True
        match self.op:
            case 'AND':
                return a & b
            case 'OR':
                return a | b
            case 'XOR':
                return a ^ b

    def __str__(self):
        op = 'bad'
        match self.op:
            case 'AND':
                op = '&'
            case 'OR':
                op = '|'
            case 'XOR':
                op = '^'

        return f"op: {self.a} {op} {self.b} = {self.out}" #, ran = {self.ran}"

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
