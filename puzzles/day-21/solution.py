import sys
import os
from itertools import permutations
from functools import cache

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

keypadPoses = {'0': (1,3), '1': (0, 2), '2': (1, 2), '3': (2, 2), '4': (0, 1), '5': (1, 1),
    '6': (2, 1), '7': (0, 0), '8': (1, 0), '9': (2, 0), 'A': (2, 3)}
controlPoses = {'A': (2, 0), '<': (0, 1), 'v': (1, 1), '>': (2, 1), '^': (1, 0)}

keyPad = set(keypadPoses.values())
controlPad = set(controlPoses.values())

deltas = {"<": (-1, 0), ">": (1, 0), "v": (0, 1), "^": (0, -1)}

"""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+

    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+
"""

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0

    codes = []

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip()
            codes.append(line)

    numRobots = 25 if part2 else 2


# TODO: find all the paths, and choose the minimum value

    for code in codes:
        # Solve Code
        numMoves = getMinCost(code, numRobots, True)

        score += numMoves * int(code[:-1])

    # Return Accumulator
    print(score)


@cache
def getMinCost(code, numRobots, atKeyPad=False):
    minCost = 0
    # Add the starting at the 'A' point
    cell = 'A'
    for newCell in code:
        possiblePaths = findAllPaths(cell, newCell, atKeyPad)
        # If at last robot, it's the keypad
        if numRobots:
            minCost += min(getMinCost(path, numRobots - 1) for path in possiblePaths)
        # Else, solve recursively
        else:
            minCost += min(len(path) for path in possiblePaths)

        # Set next value in iter
        cell = newCell

    return minCost


@cache
def findAllPaths(start, end, keypad=False):
    # Finds all paths from start to end, returning the valid ones
    poses = keypadPoses if keypad else controlPoses
    sX, sY = poses[start]
    eX, eY = poses[end]
    dX, dY = eX - sX, eY - sY

    mX = ('>' if dX > 0 else '<') * abs(dX)
    mY = ('v' if dY > 0 else '^') * abs(dY)

    paths = []
    for p in permutations(mX + mY):
        if isValidPath((sX, sY), p, keypad):
            paths.append("".join(p) + "A")

    return paths


@cache
def isValidPath(cell, path, keypad=False):
    pad = keyPad if keypad else controlPad
    # Returns true if all the moves in the path are valid
    cellX, cellY = cell
    for p in path:
        dx, dy = deltas[p]
        cellX += dx
        cellY += dy
        if (cellX, cellY) not in pad:
            return False

    return True


# TODO: Need to actually pick the best path, considering the next step, likely want the most repetition
@cache
def solveCode(code, keypad = False):
    poses = keypadPoses if keypad else controlPoses
    robotPose = 'A'
    moves = ''
    for c in code:
        moves += buildMoveStep(poses[robotPose], poses[c], keypad)
        robotPose = c

    return moves

@cache
def buildMoveStep(start, end, keypad):
    sX, sY = start
    eX, eY = end
    dX, dY = eX - sX, eY - sY
    pad = keyPad if keypad else controlPad

    # Movement commands
    # Force repeated movements
    mX = ('>' if dX > 0 else '<') * abs(dX)
    mY = ('v' if dY > 0 else '^') * abs(dY)

    moves = ''

    hFirstValid = (eX, sY) in pad
    vFirstValid = (sX, eY) in pad

    # If moving horizontally first is valid, move horizontally first
    if hFirstValid:
        moves += mX + mY
    else:
        moves += mY + mX

    # Add confirm
    moves += 'A'

    return moves


if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
