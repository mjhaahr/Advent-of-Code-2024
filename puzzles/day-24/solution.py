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
                    ops.append(Op(m.group(1), m.group(3), m.group(4), m.group(2)))

    # Run all operations
    idx = 0
    while ops:
        op = ops[idx]
        if op.a in values and op.b in values:
            values[op.out] = op.run(values[op.a], values[op.b])
            del ops[idx]

            if idx >= len(ops):
                idx = len(ops) - 1
        else:
            idx = (idx + 1) % len(ops)

    # Find All Output Values
    for out, val in values.items():
        if out[0] != 'z':
            continue

        # Shift in the output at it's position
        offset = int(out[1:3])
        score += val << offset

    # Return Accumulator
    print(score)


class Op:
    def __init__(self, a, b, out, op):
        self.a = a
        self.b = b
        self.out = out
        self.op = op
        self.ran = False

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

        return f"op: {self.a} {op} {self.b} = {self.out}, ran = {self.ran}"

    def __repr__(self):
        return str(self)

if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
