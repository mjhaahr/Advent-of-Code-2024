import sys
import os
from collections import defaultdict

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
    
    for region in regions.values():
        area = len(region)
        perimeter = findPerimeter(region, m)
        price = area * perimeter
        # print(f"Region: {m.get(list(region)[0])}, A = {area}, P = {perimeter}, Price = {price}")
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
    for plot in region:
        num = 4
        for val, x, y, offsetX, offsetY in m.getNeighborsOf4(plot):
            if (x, y) in region:
                num -= 1
                
        perimeter += num
    
    return perimeter
    
    
# Algo: run DFS to find extents of each region (saving the locations in a dict (make some way of making them unique labels), add to a set at each key)
# Then area is length of set, reconstruct the area to figure out the perimeter: for each cell, which neighbor (of 4) is in the set, sum that, that's the perimeter

    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
