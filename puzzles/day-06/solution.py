import sys
import os
from itertools import cycle

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
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
    
    start = ()
    
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val == '^':
                start = (x, y)
                break
        
        if start:
            break
            
    seen = set()
    
    dirs = cycle([[0, -1], [1, 0], [0, 1], [-1, 0]])
    
    currDir = next(dirs)
    square = start
    val = m.get(square)
    
    # Constantly loop over the list
    while(val):
        seen.add(square)
        nextSquare = tuple([x + y for x, y in zip(square, currDir)])
        val = m.get(nextSquare)
        if val == '#':
            currDir = next(dirs)
            nextSquare = tuple([x + y for x, y in zip(square, currDir)])
            
        square = nextSquare
    
    score = len(seen)
    
    # Return Accumulator    
    print(score)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
