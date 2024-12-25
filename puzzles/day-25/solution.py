import sys
import os
from itertools import product

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0

    schematics = []
    curr = []

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip()
            if line == '':
                schematics.append(curr)
                curr = []
                continue
            else:
                curr.append(line)

        schematics.append(curr)

    locks = []
    keys = []

    base = '#' * 5

    # Parse out the keys/locks
    for schem in schematics:
        if schem[0] == base:
            lock = []
            for pos in range(5):
                for cut in range(0, 6):
                    if schem[cut + 1][pos] == '.':
                        lock.append(cut)
                        break

            locks.append(lock)

        elif schem[-1] == base:
            key = []
            for pos in range(5):
                for cut in range(0, 6):
                    if schem[5 - cut][pos] == '.':
                        key.append(cut)
                        break

            keys.append(key)

    # Find combinations that do not overlap
    for lock, key in product(locks, keys):
        score += 1 if evalLock(lock, key) else 0

    # Return Accumulator
    print(score)

def evalLock(lock, key):
    for lockPin, keyPin in zip(lock, key):
        # Too big, exit
        if lockPin + keyPin >= 6:
            return False

    # If satisfied, return true
    return True


if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
