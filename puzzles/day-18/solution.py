import sys
import os
import heapq
import math
from collections import defaultdict

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    bytes = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip() 
            x, y = line.split(',')
            bytes.append((int(x), int(y)))
            
        
    # Setup the world bounds
    if "example" in filename:
        world = (6, 6)
        bytesLen = 12
    else:
        world = (70, 70)
        bytesLen = 1024
    
    """
    rows = [['.'] * (world[0] + 1) for _ in range((world[1] + 1))]
        
    for x, y in bytes:
        rows[y][x] = '#'
        
    rowstr = [''.join(row) for row in rows]
    print(*rowstr, sep='\n')
    """
    
    if not part2:
        bytes = set(bytes[:bytesLen])
        score = findPath(bytes, (0, 0), world)
    else:
        score = bytesLen
        subBytes = set(bytes[:score])
        longest = findPath(subBytes, (0, 0), world)
        while longest < math.inf:
            subBytes.add(bytes[score])
            longest = findPath(subBytes, (0, 0), world)
            score += 1
        
        # Go back by one
        score -= 1
        score = f"{bytes[score][0]},{bytes[score][1]}"
    
    # Return Accumulator    
    print(score)
    
    
def findPath(obstacles, start, world):
    # Runs Dijkstra
    
    costs = defaultdict(lambda: math.inf)
    costs[(start)] = 0
    prevs = {}
    
    # Priority Cell queue
    cells = []
    heapq.heappush(cells, (0, start))
    while cells:
        cost, cell = heapq.heappop(cells)
        
        for newCell in getNextCells(cell, world, obstacles):
            newCost = cost + 1
            
            # If the new cost is less than the current cost
            if newCost < costs[newCell]:
                costs[newCell] = newCost
                # And add to the priority queue
                heapq.heappush(cells, (newCost, newCell))
                prevs[newCell] = cell
    
    score = costs[world]
    
    return score
    
    
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
    
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
