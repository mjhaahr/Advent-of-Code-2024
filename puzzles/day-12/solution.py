import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    strs = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip() 
            
            strs.append([c for c in line])
            
    m = utils.Grid(strs)
    regions = findRegions(m)
    
    print(m)
    
    for region in regions.values():
        area = len(region)
        if not part2:
            perimeter = findPerimeter(region, m)
            price = area * perimeter
            # print(f"Region: {m.get(list(region)[0])}, A = {area}, P = {perimeter}, Price = {price}")
        else:
            sides = findSides(region, m)
            price = area * sides
            print(f"Region: {m.get(list(region)[0])}, A = {area}, S = {sides}, Price = {price}\n")
        score += price
    
    # Return Accumulator    
    print(score)
    
# Builds a dictionary of region
def findRegions(m):
    regions = {}
    
    num = 0
    
    for y, row in enumerate(m):
        for x, val in enumerate(row):
            # If already in the region, it's not open
            skip = False
            for regionSet in regions.values():
                if (x, y) in regionSet:
                    skip = True
                    break
                    
            if not skip:      
                locs = findRegion((x,y), val, m)
                regions[num] = locs
                num += 1
    
    return regions
    
    
# Finds the Region
def findRegion(point, target, m):
    locs = set()
    
    cellStack = [point]
    while cellStack:
        cell = cellStack.pop()
        
        # If the value is correct (and new), add to the set and find the neighbors
        if cell in locs:
            continue
        elif m.get(cell) == target:
            locs.add(cell)
            for val, x, y, offsetX, offsetY in m.getNeighborsOf4(cell):
                cellStack.append((x, y))
    
    
    return locs
    

# Finds the perimeter of a region
def findPerimeter(region, m):
    perimeter = 0
    for cell in region:
        num = 4
        for val, x, y, offsetX, offsetY in m.getNeighborsOf4(cell):
            if (x, y) in region:
                num -= 1
                
        perimeter += num
    
    return perimeter
    

# Finds the number of unique sides of a region
def findSides(region, m):
    start = findCorner(region)
    sides = 0
    
    square = ()
    offset = []
    # Up and left are only directions this can go
    for d in [(-1, 0), (0, -1)]:
        if (start[0] + d[0], start[1] + d[1]) in region:
            square = (start[0] + d[0], start[1] + d[1])
            offset = d
          
    # Single element  
    if not square:
        sides = 4
    else:
        # Loop: check square right then fwd then left if they are in the region (save the offset)
            # if not fwd, incr sides
            # Follow path until back at start
        sides = 1
        first = offset
        while True:
            # End when back at start
            if square == start:
                break
            
            rightDir = utils.getRight(offset)
            rightSquare = (square[0] + rightDir[0], square[1] + rightDir[1])
            
            fwdSquare = (square[0] + offset[0], square[1] + offset[1])
            
            leftDir = utils.getLeft(offset)
            leftSquare = (square[0] + leftDir[0], square[1] + leftDir[1])
            
            if rightSquare in region:
                sides += 1
                offset = rightDir
            elif fwdSquare in region:
                # No change
                pass
            elif leftSquare in region:
                sides += 1
                offset = leftDir
            else:
                # Have to turn around
                sides += 2
                offset = (-offset[0], -offset[1])
                
            square = (square[0] + offset[0], square[1] + offset[1])
            
        while offset != utils.getRight(first):
            sides += 1
            offset = utils.getLeft(offset)
    
    return sides

# Finds the bottom right most corner of
def findCorner(region):
    corner = (0, 0)
    for cell in region:
        if cell[0] >= corner[0] and cell[1] >= corner[1]:
            corner = cell
        
    return corner
    
    

# Algo: run DFS to find extents of each region (saving the locations in a dict (make some way of making them unique labels), add to a set at each key)
# Then area is length of set, reconstruct the area to figure out the perimeter: for each cell, which neighbor (of 4) is in the set, sum that, that's the perimeter
# Sides: find corner, hug a wall, each turn taken is a new side
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
