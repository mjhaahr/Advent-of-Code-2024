import sys
import os
import math
import heapq
from collections import defaultdict

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    lines = []
    start = ()
    end = ()
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for y, line in enumerate(fp.readlines()):
            line = line.strip()
            l = []
            for x, c in enumerate(line):
                l.append(c)
                if c == 'S':
                    start = (x, y)
                elif c == 'E':
                    end = (x, y)
                    
            lines.append(l)
                
                
            
    maze = utils.Grid(lines)
    
    score = findPath(maze, start, end, part2)
    
    # Return Accumulator    
    print(score)
    
def findPath(maze, start, end, part2):
    # Runs Dijkstra, effectively, but store rotation as a step
    
    costs = defaultdict(lambda: math.inf)
    costs[(start, (1, 0))] = 0
    prevs = defaultdict(set)
    
    pathCost = math.inf
    
    # Priority Cell queue
    cells = []
    # Store direction that was came from (with the start)
    heapq.heappush(cells, (0, (start, (1, 0))))
    while cells:
        cost, cellData = heapq.heappop(cells)
        cell = cellData[0]
        d = cellData[1]
        
        # If at end, update the stored cost
        if cell == end:
            if cost < pathCost:
                pathCost = cost
        
        for newCellData, constIncr in getNextCells(maze, cell, d):
            newCost = cost + constIncr
            # If the new cost is less than the current cost
            if newCost < costs[newCellData]:
                costs[newCellData] = newCost
                # And add to the priority queue
                heapq.heappush(cells, (newCost, newCellData))
                prevs[newCellData] = {cellData}
            # If equal, add to the set
            elif newCost == costs[newCellData]:
                prevs[newCellData].add(cellData)
    
    if not part2:
        score = pathCost
    else:
        score = 0    
    
    return score
    
# Yields the optional turns then the straight ahead: (cell, dir), cost
def getNextCells(maze, cell, d):
    yield (cell, utils.getRight(d)), 1000
    yield (cell, utils.getLeft(d)), 1000
    nextCell = (cell[0] + d[0], cell[1] + d[1])
    if maze.get(nextCell) != '#':
        yield (nextCell, d), 1

    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
