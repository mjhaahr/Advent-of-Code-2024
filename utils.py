class Grid:
    def __init__(self, grid):
        self.bounds = [len(grid[0]) - 1, len(grid) - 1]
        self.grid = grid
        self.__gridIter = iter(grid)
    
    # Returns item at grid cell, else returns None
    def get(self, x, y = 0):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            y = x[1]
            x = x[0]
        
        # If at a bounds, skip, cannot be valid there
        if x < 0 or y < 0 or x > self.bounds[0] or y > self.bounds[1]:
            return None
        else:
            return self.grid[y][x]
    
    # Attempts to set a value, if cannot, returns false   
    def set(self, x, y, val = 0):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            val = y
            y = x[1]
            x = x[0]
            
        # If at a bounds, skip, cannot be valid there
        if x < 0 or y < 0 or x > self.bounds[0] or y > self.bounds[1]:
            return False
        else:
            self.grid[y][x] = val
            return True
        
    def __str__(self):
        rowStrs = []
        for row in self.grid:
            rowStrs.append("".join(list(str(i) for i in row)))
            
        return f"Grid:\nBounds: [0, 0] to {self.bounds}\n  {"\n  ".join(rowStrs)}\n"
        
    def __repr__(self):
        return str(self)
        
    def __iter__(self):
        return self
        
    def __next__(self):
        return next(self.__gridIter)
        
    # returns all neighbors (of 8) in the format [val, x, y, offsetX, offsetY]
    def getNeighborsOf8(self, x, y=0):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            val = y
            y = x[1]
            x = x[0]
            
        neighbors = []
        # Get all Surrounding Cells
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                # If at the center, skip
                if i == 0 and j == 0:
                    continue
                
                newX = x + i
                newY = y + j
                neighbors.append([self.get(newX, newY), newX, newY, i, j])
        
        return neighbors
        
    # returns all valid neighbors (of 4) in the format [[val, x, y, offsetX, offsetY] (order is U, L, D, R)
    def getNeighborsOf4(self, x, y=0):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            val = y
            y = x[1]
            x = x[0]
            
        neighbors = []
        # Get all Surrounding Cells
        for i, j in [[0, -1], [1, 0], [0, 1], [-1, 0]]:
            newX = x + i
            newY = y + j
            neighbors.append([self.get(newX, newY), newX, newY, i, j])
        
        return neighbors
    
    # returns all valid neighbors (of 4 Rotated) in the format [val, x, y, offsetX, offsetY] (order is UL, UR, DL, DR)
    def getNeighborsOf4Rot(self, x, y=0):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            val = y
            y = x[1]
            x = x[0]
            
        neighbors = []
        # Get all Surrounding Cells
        for j in [-1, 1]:
            for i in [-1, 1]:
                newX = x + i
                newY = y + j
                neighbors.append([self.get(newX, newY), newX, newY, i, j])
        
        return neighbors
        
dirList = [(0, -1), (1, 0), (0, 1), (-1, 0)]

def addDir(cell, d):
    return (cell[0] + d[0], cell[1] + d[1])

def getRight(d):
    d = (d[0], d[1])
    idx = dirList.index(d)
    idx = (idx + 1) % 4
    return dirList[idx]
    
    
def getLeft(d):
    d = (d[0], d[1])
    idx = dirList.index(d)
    idx = (idx + 3) % 4
    return dirList[idx]
            
