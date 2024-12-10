import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    topo = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        line = fp.readline().strip()
        while line:
            
            topo.append(list(int(c) for c in line))
            
            line = fp.readline().strip()  
            
    m = utils.Grid(topo)
    
    # Find all trailheads (0)
    trailheads = []
            
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            if val == 0:
                trailheads.append((x, y))
    
    # Loop over all trailheads
    for trailhead in trailheads:
        if not part2:
            score += findScore(trailhead, m)
        else:
            score += findRating(trailhead, m)
    
    # Return Accumulator    
    print(score)
    
# Finds the score of the given trailhead (runs DFS to find all ends)
def findScore(trailhead, m):
    # Use a set of visited ends, e.g. return the length of the set
    visited = set()
    
    cellStack = [trailhead]
    while cellStack:
        cell = cellStack.pop()
        for val, x, y, offsetX, offsetY in m.getNeighborsOf4(cell[0], cell[1]):
            # If the neighbor is one greater, it's walkable
            if val == (m.get(cell)) + 1:
                # at end
                if val == 9:
                    visited.add((x, y))
                # valid cell, add to stack
                elif val:
                    cellStack.append((x, y))
    
    
    return len(visited)
    
# Finds the unique trails from one trailhead
def findRating(trailhead, m):
    # Rating is just a sum
    rating = 0
    
    cellStack = [trailhead]
    while cellStack:
        cell = cellStack.pop()
        for val, x, y, offsetX, offsetY in m.getNeighborsOf4(cell[0], cell[1]):
            # If the neighbor is one greater, it's walkable
            if val == (m.get(cell)) + 1:
                # at end
                if val == 9:
                    rating += 1
                    # valid cell, means we found a unique path
                elif val:
                    cellStack.append((x, y))
    
    
    return rating
    
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
