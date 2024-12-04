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
    def set(self, x, y, val):
        # Pull out coords from a tuple or list
        if (type(x) == list or type(x) == tuple):
            y = x[1]
            x = x[0]
            
        # If at a bounds, skip, cannot be valid there
        if x <= 0 or y <= 0 or x >= bounds[0] or y >= bounds[1]:
            return False
        else:
            self.grid[y][x] = val
            return True
        
    def __str__(self):
        rowStrs = []
        for row in self.grid:
            rowStrs.append(", ".join(row))
            
        return f"Grid:\n  {"\n  ".join(rowStrs)}\n"
        
    def __repr__(self):
        return self.__str__()
        
    def __iter__(self):
        return self
        
    def __next__(self):
        return next(self.__gridIter)
        
            
