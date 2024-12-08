import sys
import os
from itertools import cycle
from copy import deepcopy as copy

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero Accumulator
    score = 0

    strs = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        line = fp.readline()
        while line:
                   
            strs.append(list(c for c in line if not c.isspace()))
            
            line = fp.readline()
            
    m = utils.Grid(strs)
    
    start = {}
    
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val == '^':
                start = (x, y)
                break
        
        if start:
            break
            
    visited = {}
    
    dirs = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])
    
    currDir = next(dirs)
    square = start
    val = m.get(square)
    
    # Constantly loop over the list to create the path
    while(val):
        visits = visited.get(square, set())
        visits.add(currDir)
        visited[square] = visits 
        
        nextSquare = tuple([x + y for x, y in zip(square, currDir)])
        nextVal = m.get(nextSquare)
        if nextVal == '#':
            currDir = next(dirs)
            nextSquare = tuple([x + y for x, y in zip(square, currDir)])
           
        square = nextSquare
        val = m.get(square)
    
    if not part2:
        score = len(visited)
    else:
        # Run part 2 to find if an obstacle placed at any point along the path will loop
        for loc in visited.keys():
            # To find obstacles, count times a perpendicular ray (from the right) of the current direction of travel intersects a path, then the obstacle is the next square, sum num obstacles, has to be uninterrupted
            
            # Cannot run with obstacle where guard starts
            if loc == start:
                continue
            
            # Set the obstacle
            m.set(loc, 'O')
            
            dirs = cycle([(0, -1), (1, 0), (0, 1), (-1, 0)])
            score += findLoopedPath(start, dirs, m)
            
            # Unset the obstacle
            m.set(loc, '.')
    
    # Return Accumulator    
    print(score)
    
   
# Returns 1 if path loops 
def findLoopedPath(start, dirs, m):
    # Find if placing an obstacle in front of the current path will cause the path to loop
    currDir = next(dirs)
    square = start
    val = m.get(square)
    
    visited = {}
    
    while val:
        # Add current element to the list of visited cells (and directions)
        visits = visited.get(square, set())
        # Check if already visited this cell
        if currDir in visits:
            return 1
        
        visits.add(currDir)
        visited[square] = visits
        
        # Look ahead down the path
        nextSquare = tuple([x + y for x, y in zip(square, currDir)])
        nextVal = m.get(nextSquare)
        # If blocked (existing blockage or the obstacle), turn
        if nextVal == '#' or nextVal == 'O':
            currDir = next(dirs)
            nextSquare = tuple([x + y for x, y in zip(square, currDir)])
        
        # Advance down the path
        square = nextSquare
        val = m.get(square)
    
    return 0  
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
