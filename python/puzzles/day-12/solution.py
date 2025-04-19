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
    
    # print(m)
    
    for region in regions.values():
        area = len(region)
        if not part2:
            perimeter = findPerimeter(region, m)
            price = area * perimeter
            # print(f"Region: {m.get(list(region)[0])}, A = {area}, P = {perimeter}, Price = {price}")
        else:
            sides = findSides(region, m)
            price = area * sides
            # print(f"Region: {m.get(list(region)[0])}, A = {area}, S = {sides}, Price = {price}\n")
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
    # Find top and bottom extents of Grid
    # Find left and right extents of Grid
    # Loop over each, finding where there are new edges for each
    
    sides = 0
    extents = findExtents(region, m)
    newRegion = rebuildRegion(region, extents)
    
    # Need to find continuities as well
      
    # Top edges
    currEdges = [0] * (extents[1] - extents[0] + 1)      
    for y in range(len(newRegion)):
        newEdges = [0] * (extents[1] - extents[0] + 1)
        for x in range(len(newRegion[y])):
            newEdges[x] = newRegion[y][x]
            
        for idx, (i, j) in enumerate(zip(currEdges, newEdges)):
            # Was not occupied, now occupied
            if (i == 0 and j == 1):
                currEdges[idx] = 1
            else:
                currEdges[idx] = 0
        
        state = False
        for edge in currEdges:
            if state == False and edge == 1:
                state = True
                sides += 1
            elif state == True and edge == 0:
                state= False
                
        currEdges = newEdges
        
    # Bottom edges
    currEdges = [0] * (extents[1] - extents[0] + 1)      
    for y in range(len(newRegion) - 1, -1, -1):
        newEdges = [0] * (extents[1] - extents[0] + 1)
        for x in range(len(newRegion[y]) - 1, -1, -1):
            newEdges[x] = newRegion[y][x]
            
        for idx, (i, j) in enumerate(zip(currEdges, newEdges)):
            if (i == 0 and j == 1):
                currEdges[idx] = 1
            else:
                currEdges[idx] = 0
        
        state = False
        for edge in currEdges:
            if state == False and edge == 1:
                state = True
                sides += 1
            elif state == True and edge == 0:
                state= False
                
        currEdges = newEdges
                
    # Left edges
    currEdges = [0] * (extents[3] - extents[2] + 1)      
    for x in range(len(newRegion[y])):
        newEdges = [0] * (extents[3] - extents[2] + 1)
        for y in range(len(newRegion)):
            newEdges[y] = newRegion[y][x]
            
        for idx, (i, j) in enumerate(zip(currEdges, newEdges)):
            # Was not occupied, now occupied
            if (i == 0 and j == 1):
                currEdges[idx] = 1
            else:
                currEdges[idx] = 0
        
        state = False
        for edge in currEdges:
            if state == False and edge == 1:
                state = True
                sides += 1
            elif state == True and edge == 0:
                state= False
                
        currEdges = newEdges
        
    # Right edges
    currEdges = [0] * (extents[3] - extents[2] + 1)      
    for x in range(len(newRegion[y]) - 1, -1, -1):
        newEdges = [0] * (extents[3] - extents[2] + 1)
        for y in range(len(newRegion) - 1, -1, -1):
            newEdges[y] = newRegion[y][x]
            
        for idx, (i, j) in enumerate(zip(currEdges, newEdges)):
            if (i == 0 and j == 1):
                currEdges[idx] = 1
            else:
                currEdges[idx] = 0
        
        state = False
        for edge in currEdges:
            if state == False and edge == 1:
                state = True
                sides += 1
            elif state == True and edge == 0:
                state= False
                
        currEdges = newEdges
    
    return sides
    
    
# Rebuilds the region into a 2d array (of 1s and 0s, for easier parsing)
def rebuildRegion(region, extents):
    newRegion = [[0] * (extents[1] - extents[0] + 1) for _ in range((extents[3] - extents[2] + 1))]
    offsetX = extents[0]
    offsetY = extents[2]
    
    for x, y in region:
        newRegion[y - offsetY][x - offsetX] = 1
    
    return newRegion
    

# Edges of the Grid (left, right, top, bottom)
def findExtents(region, m):
    # Work towards center
    extents = [m.bounds[0], 0, m.bounds[1], 0]
    for cell in region:
        extents[0] = cell[0] if cell[0] < extents[0] else extents[0]
        extents[1] = cell[0] if cell[0] > extents[1] else extents[1]
        
        extents[2] = cell[1] if cell[1] < extents[2] else extents[2]
        extents[3] = cell[1] if cell[1] > extents[3] else extents[3]
        
    return extents
    
    

# Algo: run DFS to find extents of each region (saving the locations in a dict (make some way of making them unique labels), add to a set at each key)
# Then area is length of set, reconstruct the area to figure out the perimeter: for each cell, which neighbor (of 4) is in the set, sum that, that's the perimeter
# Sides:
    # Find top and bottom extents of Grid
    # Find left and right extents of Grid
    # Loop over each, finding where there are new edges for each
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
