import sys
import os
from math import inf
from collections import defaultdict, deque
from itertools import product

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0

    obstacles = set()

    # Default defines
    world = [0, 0]
    start = [0, 0]
    end = [0, 0]

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for y, line in enumerate(fp.readlines()):
            world[1] = y
            line = line.strip()
            for x, val in enumerate(line):
                if x > world[0]:
                    world[0] = x

                cell = (x, y)
                # If Obstacle
                if val == '#':
                    obstacles.add(cell)
                elif val == 'S':
                    start = cell
                elif val == 'E':
                    end = cell

    # Algorithm:
    # Find all paths from start to each point and from end to each point (distance is the sum)
    # For each OPEN point in the grid, find all points up to DIST away, find the new distance

    fromStart = findPath(obstacles, start, world)
    fromEnd = findPath(obstacles, end, world)

    # Base Path Length: Length from start to end
    basePath = fromStart[end]

    if not part2:
        skip = 2
    else:
        skip = -1

    # All Cells
    for cell in product(range(world[0]), range(world[1])):
        # All Open Cells
        if cell not in obstacles:
            # Find the cell with a cheat
            for x, y in findCellsWithInDist(cell, skip):
                newCell = (x, y)
                # Cell is not an obstacle
                if newCell in obstacles:
                    continue
                # Check if the cell is in the world
                elif x < 0 or y < 0 or x > world[0] or y > world[1]:
                    continue
                else:
                    dist = calcDist(cell, newCell)
                    cheat = fromStart[cell] + dist + fromEnd[newCell]

                    if cheat <= basePath - 100:
                        score += 1

    # Return Accumulator
    print(score)


def findPath(obstacles, start,  world):
    # Runs BFS to find the path
    seen = defaultdict(lambda: inf)
    seen[(start)] = 0
    prevs = {}

    # Priority Cell queue
    cells = deque([start])
    while cells:
        cell = cells.popleft()
        for newCell in getNextCells(cell, world, obstacles):
            # If the new cost is less than the current cost
            if newCell in seen:
                continue
            else:
                seen[newCell] = seen[cell] + 1
                cells.append(newCell)
    return seen


def getNextCells(cell, world, obstacles):
    for d in utils.dirList:
        newCell = utils.addDir(cell, d)
        x, y = newCell
        # Check if the cell is an obstacle
        if newCell in obstacles:
            continue
        # Check if the cell is in the world
        elif x < 0 or y < 0 or x > world[0] or y > world[1]:
            continue
        # Else, yield the cell
        else:
            yield newCell


def findCellsWithInDist(cell, dist):
    # Effectively create the "circle" around the cell
    # Find the box around the cell
    for delta in product(range(-dist, dist + 1), repeat=2):
        # Skip center
        if delta == (0, 0):
            continue
        if (abs(delta[0]) + abs(delta[1])) <= dist:
            yield utils.addDir(cell, delta)


def calcDist(a, b):
    delta = (a[0] - b[0], a[1] - b[1])
    return abs(delta[0]) + abs(delta[1])


def printMap(world, start, end, obstacles, path=[]):
    # Setup world
    rows = [['.'] * (world[0] + 1) for _ in range((world[1] + 1))]
    # Add obstacles
    for x, y in obstacles:
        rows[y][x] = '#'
    # Add Oath
    for x, y in path:
        rows[y][x] = 'O'
    # Add start and end
    rows[start[1]][start[0]] = 'S'
    rows[end[1]][end[0]] = 'E'

    rowstr = [''.join(row) for row in rows]
    print(*rowstr, sep='\n')
    print("")

if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
