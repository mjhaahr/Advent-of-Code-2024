import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    m = Map()
    
    dirs = []
    dirDecode = {'^': (0, -1), 'v': (0, 1), '<': (-1, 0), '>': (1, 0)}
    
    # Open File
    with open(filename, 'r') as fp:
        loadMap = False
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip() 
            
            if loadMap:
                m.addRow(line)
            else:
                if line and line[0] != '#':
                    for c in line:
                        dirs.append(dirDecode[c])
            
            if line and all(c == '#' for c in line):
                loadMap = not loadMap
                if loadMap:
                    m.addRow(line)
                
        m.addFinished()
        
        
    #print(m)
    # TODO: parse map (make obstacle '#', box (can be slid until obstacle 'O'), and person '@')
    # Then combine the directions into a queue, and continually pop the front
    # For each box, sum the GPS loc (100 * y + x) (maybe offset by one for each loc)
    
    #print(m)
    for step, d in enumerate(dirs):
        m.move(d)
        #print(f"Step: {step + 1}")
        #print(m)
        
    score = m.getScore()
    
    # Return Accumulator    
    print(score)
    

class Map:
    def __init__(self):
        self.bounds = [0, 0]
        self.obstacles = set()
        self.boxes = set()
        self.player = ()
        self.init = False
        
    # Returns true if valid
    def addRow(self, row):
        if self.bounds[0] > 0:
            if len(row) != self.bounds[0]:
                return False
        else:
            self.bounds[0] = len(row)

        y = self.bounds[1]
        self.bounds[1] += 1
        
        for x, c in enumerate(row):
            if c == '#':
                self.obstacles.add((x, y))
            elif c == 'O':
                self.boxes.add((x, y))
            elif c == '@':
                self.player = (x, y)
            
        return True
        
    def addFinished(self):
        self.init = True
        
    # Dir to move, if player, if not, need loc
    # Returns true if could make the move, false if couldn't
    def move(self, d, p = True, loc = (0, 0)):
        if p:
            loc = self.player
            
        newPos = (loc[0] + d[0], loc[1] + d[1])
        # Look in obstacles
        if newPos in self.obstacles:
            return False
        # Look in boxes
        elif  newPos in self.boxes:
            canMove = self.move(d, False, newPos)
        # Else open space
        else:
            canMove = True
            
        if canMove:
            # If the player, move it
            if p:
                self.player = newPos
            # If a box, remove it and update the boxes
            else:
                self.boxes.remove(loc)
                self.boxes.add(newPos)
        
        return canMove
    
    # sum the GPS loc of each box (100 * y + x)   
    def getScore(self):
        score = 0
        
        for box in self.boxes:
            score += 100 * box[1] + box[0]
        
        return score
                
        
    def __str__(self):
        grid = [['.'] * self.bounds[0] for _ in range(self.bounds[1])]
        grid[self.player[1]][self.player[0]] = '@'
        
        for obstacle in self.obstacles:
            grid[obstacle[1]][obstacle[0]] = '#'
            
        for box in self.boxes:
            grid[box[1]][box[0]] = 'O'
            
        rowStrs = []
        for row in grid:
            rowStrs.append("".join([str(i) for i in row]))
            
        gridStr = "  \n".join(rowStrs)
        
        return f"Map: {self.init}\nScore: {self.getScore}\n{gridStr}\n\n  Player: {self.player}\n  Obstacles: {self.obstacles}\n  Boxes: {self.boxes}\n"
        
    def __repr__(self):
        return str(self)
        
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
