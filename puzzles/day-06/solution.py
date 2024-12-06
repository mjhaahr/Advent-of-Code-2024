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
        while True:
            # Loop over all lines
            line = fp.readline()
            
            # EOF check
            if line == '':
                break   
                   
            strs.append(list(c for c in line if not c.isspace()))
            
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
    
    dirList = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dirs = cycle(dirList)
    
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
            
        # If not blocked, run part 2  
        elif part2:
            # To find obstacles, count times a perpendicular ray (from the right) of the current direction of travel intersects a path, then the obstacle is the next square, sum num obstacles, has to be uninterrupted
            
            # TODO: Rewrite this shit and clean it up
            
            lookAheadVisited = copy(visited)
            lookAheadDirs = copy(dirs)
            
            # Set the obstacle
            m.set(nextSquare, '#')
            
            # Look to the right
            targetDir = next(lookAheadDirs)
            # Start path
            lookSquare = tuple([x + y for x, y in zip(square, targetDir)])
            lookVal = m.get(lookSquare)
            while lookVal:
                # Advance down the path
                newVisits = lookAheadVisited.get(lookSquare, set())
                newVisits.add(targetDir)
                lookAheadVisited[lookSquare] = newVisits
                # If blocked, need to trun
                if lookVal == '#':
                    targetDir = next(lookAheadDirs)
                    lookSquare = tuple([x + y for x, y in zip(lookSquare, targetDir)])
                    lookVal = m.get(lookSquare)
                # If not blocked, look for previous visits (in that direction)
                elif targetDir in newVisits:
                    score += 1
                    break
                # Else, keep looking
                else:
                    lookSquare = tuple([x + y for x, y in zip(lookSquare, targetDir)])
                    lookVal = m.get(lookSquare)
                    
            # unset the obstacle
            m.set(nextSquare, '.')
            
        square = nextSquare
        val = m.get(square)
    
    if not part2:
        score = len(visited)
    
    # Return Accumulator    
    print(score)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
