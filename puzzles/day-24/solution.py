import sys
import os
import re

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
        # Remove the ops from savedOps for time savings
        adder = [addOp, carryOp]
        for op in adder:
            ops.remove(op)

        for i in range(1, maxZ):
            good, adder = evalRipple(cOut, ops, i)
            if debug: print(good, adder)
            # Remove the ops from savedOps for time savings
            if good:
                cOut = adder[-1].out
                for op in adder:
                    ops.remove(op)
            else:
                print(f"Error at {i}")
                break
                # TODO find swap
                # Only occurs within the swap, rather than outside of it

        # Last cOut should be z[maxZ]
        good = cOut == f"z{maxZ:02d}"
        print(good)

    # Return Accumulator
    print(score)


# Returns if the adder is good and the operations to create the full adder (if good)
# If the Order: Half Add, Full Add, Half Carry, Factor In, Full Carry
def evalRipple(cIn, ops, idx, debug=False):
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
            if x in op.args and y in op.args:
                if op.op == 'XOR':
                    halfAdd = op
                    if debug: print("found Half Add")
                elif op.op == 'AND':
                    halfCarry = op
                    if debug: print("found Half Carry")
            if halfAdd is not None and halfCarry is not None:
                break

        for op in ops:
            if halfAdd.out in op.args and cIn in op.args:
                if op.op == 'XOR':
                    fullAdd = op
                    if debug: print("found Full Add")
                elif op.op == 'AND':
                    factorIn = op
                    if debug: print("found Factor In")
            if fullAdd is not None and factorIn is not None:
                break

        for op in ops:
            if factorIn.out in op.args and halfCarry.out in op.args:
                if op.op == 'OR':
                    fullCarry = op
                    if debug: print("found Full Carry")
                    break

    except AttributeError:
        return False, []

    #print(f"Half Add {halfAdd}\nFull Add {fullAdd}\nHalf Carry {halfCarry}\nFactor In {factorIn}\nFull Carry {fullCarry}\n")

    if fullAdd.out == f"z{idx:02d}":
        return True, [halfAdd, fullAdd, halfCarry, factorIn, fullCarry]
    else:
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
