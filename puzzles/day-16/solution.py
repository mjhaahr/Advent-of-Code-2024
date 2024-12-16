import sys
import os
import math
import heapq

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
    
    score = findPath(maze, start, end)
    
    # Return Accumulator    
    print(score)
    
def findPath(maze, start, end):
    # Runs Dijkstra, effectively
    dirs = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    
    costs = {start: 0}
    prevs = {start: None}
    
    # Priority Cell queue
    cells = []
    # Store direction that was came from (with the start)
    heapq.heappush(cells, (0, [start, (1, 0)]))
    while cells:
        cellData = heapq.heappop(cells)[1]
        cell = cellData[0]
        d = cellData[1]
        
        # If at end, do not process
        if cell == end:
            continue
        
        for val, x, y, offsetX, offsetY in maze.getNeighborsOf4(cell):
            nextCell = (x, y)
            newDir = (offsetX, offsetY)
            # If the prior cell to this one is the current cell, ignore
            if nextCell == prevs.get(cell, False):
                continue
            # If not a wall, add to the list 
            if val != '#':
                # Get the cost of the current cell + 1
                cost = costs.get(cell) + 1
                # If direction needs to change, add 1000 to the cost
                if d != newDir:
                    # If first, ignore
                    cost += 1000
                
                # If the existing cost is greater than new (default val is infinity), replace with new
                if costs.get(nextCell, math.inf) > cost:
                    costs[nextCell] = cost
                    prevs[nextCell] = cell
                    heapq.heappush(cells, (cost, [nextCell, newDir]))

    # Not rebuilding path, currently un-needed
    """
    path = [end]
    currCell = end
    while currCell != start:
        currCell = prevs[currCell]
        path.append(currCell)
        
    path.reverse()
    print(path)
    """
    
    return costs[end]
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
