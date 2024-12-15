import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

debug = False
inter = True

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
                        dirs.append(c)
            
            if line and all(c == '#' for c in line):
                loadMap = not loadMap
                if loadMap:
                    m.addRow(line)
                
        m.addFinished()
    
    
    if part2:
        m.widen()
    
    for step, d in enumerate(dirs):
        if debug:
            if inter:
                os.system('cls' if os.name == 'nt' else 'clear')
            print(m)
            print(f"Step: {step + 1}: {d}")
            if inter:
                input()
                
        decodeDir = dirDecode[d]
        m.move(decodeDir, part2)
        
    if debug:
        if inter:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(m)
        print(f"End")
        if inter:
            input()
        
    score = m.getScore()
    
    # Return Accumulator    
    print(score)
    

class Map:
    def __init__(self):
        self.bounds = [0, 0]
        self.obstacles = set()
        self.boxes = {}
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
                self.boxes[(x, y)] = 'O'
            elif c == '@':
                self.player = (x, y)
            
        return True
        
    def addFinished(self):
        self.init = True
        
    # Dir to move, if player, if not, need loc
    # Returns true if could make the move, false if couldn't
    def move(self, d, part2, p = True, loc = (0, 0)):
        if p:
            loc = self.player
        
        if debug and not inter:   
            print(f"Checking: {'player' if p else 'box'} @ {loc}")
            
        newPos = (loc[0] + d[0], loc[1] + d[1])
        # If not part2 or is the player
        if not part2 or p:
            # Look in obstacles
            if newPos in self.obstacles:
                return False
            # Look in boxes
            elif newPos in self.boxes:
                canMove = self.move(d, part2, False, newPos)
            # Else open space
            else:
                canMove = True
        else:
            val = self.boxes.get(loc, False)
            # If looking up or down, need to look at two square (newPos and offsetNew)
            if d == (0, -1) or d == (0, 1):
                # If a box in part 2
                if val == '[':
                    offsetLoc = (loc[0] + 1, loc[1])
                    offsetNew = (newPos[0] + 1, newPos[1])
                else:
                    offsetLoc = (loc[0] - 1, loc[1])
                    offsetNew = (newPos[0] - 1, newPos[1])
                
                valNew = self.boxes.get(newPos, False)
                valOffset = self.boxes.get(offsetNew, False)
                
                # If either the one directly ahead or next to directly ahead are in obstacles
                if newPos in self.obstacles or offsetNew in self.obstacles:
                    return False
                # Look in boxes
                elif valNew or valOffset:
                    # If running part2, look ahead can depend on boxes
                    # if looking up or down, need to look at two squares (if a box)
                    if val == valNew:
                        canMove = self.move(d, part2, False, newPos)
                    else:
                        canMoveAhead = True
                        canMoveOffset = True
                        
                        # This is an issue, need to actually run a look ahead (e.g. canMove, because this splits moves one even if the other stops it)
                        if valNew:
                            canMoveAhead = self.checkCanMove(d, part2, False, newPos)
                        if valOffset:
                            canMoveOffset = self.checkCanMove(d, part2, False, offsetNew)
                        
                        # If move can move, now apply the move
                        if canMoveAhead and canMoveOffset:
                            canMove = True
                            if valNew:
                                canMoveAhead = self.move(d, part2, False, newPos)
                            if valOffset:
                                canMoveOffset = self.move(d, part2, False, offsetNew)
                            
                        else:
                            canMove = False
                
                # Else open space
                else:
                    canMove = True
            
            # If looking left or right, might need to look at an offset position
            else:
                # if looking left
                if d == (-1, 0):
                    # If '[', look at next
                    if val == '[':
                        posToCheck = newPos
                    # Else, look at the offset
                    else:
                        posToCheck = (newPos[0] - 1, newPos[1])
                else:
                    # If ']', look at next
                    if val == ']':
                        posToCheck = newPos
                    # Else, look at the offset
                    else:
                        posToCheck = (newPos[0] + 1, newPos[1])
                    
                checkVal = self.boxes.get(posToCheck, False)
                if posToCheck in self.obstacles:
                    return False
                elif checkVal:
                    canMove = self.move(d, part2, False, posToCheck)
                # Else open space
                else:
                    canMove = True
                    
            
        if canMove:
            # If the player, move it
            if p:
                self.player = newPos
            # If a box, remove it and update the boxes
            else:
                if not part2:
                    self.boxes.pop(loc)
                    self.boxes[newPos] = 'O'
                else:
                    if self.boxes.get(loc, None) == '[':
                        offsetLoc = (loc[0] + 1, loc[1])
                        offsetNew = (newPos[0] + 1, newPos[1])
                        self.boxes.pop(loc)
                        self.boxes.pop(offsetLoc)
                        self.boxes[newPos] = '[' 
                        self.boxes[offsetNew] = ']' 
                    else:
                        offsetLoc = (loc[0] - 1, loc[1])
                        offsetNew = (newPos[0] - 1, newPos[1])
                        self.boxes.pop(loc)
                        self.boxes.pop(offsetLoc)
                        self.boxes[newPos] = ']' 
                        self.boxes[offsetNew] = '[' 
                    
        
        return canMove
    
    # A look ahead to see if all affected cells can move
    def checkCanMove(self, d, part2, p = True, loc = (0, 0)):
        if p:
            loc = self.player
        
        canMove = False
        newPos = (loc[0] + d[0], loc[1] + d[1])
        # If not part2 or is the player
        if not part2 or p:
            # Look in obstacles
            if newPos in self.obstacles:
                pass
            # Look in boxes
            elif newPos in self.boxes:
                canMove = self.canMove(d, part2, False, newPos)
            # Else open space
            else:
                canMove = True
        
        else:  
            val = self.boxes.get(loc, False)
            # If looking up or down, need to look at two square (newPos and offsetNew)
            if d == (0, -1) or d == (0, 1):
                # If a box in part 2
                if val == '[':
                    offsetLoc = (loc[0] + 1, loc[1])
                    offsetNew = (newPos[0] + 1, newPos[1])
                else:
                    offsetLoc = (loc[0] - 1, loc[1])
                    offsetNew = (newPos[0] - 1, newPos[1])
                
                valNew = self.boxes.get(newPos, False)
                valOffset = self.boxes.get(offsetNew, False)
                
                # If either the one directly ahead or next to directly ahead are in obstacles
                if newPos in self.obstacles or offsetNew in self.obstacles:
                    canMove = False
                # Look in boxes
                elif valNew or valOffset:
                    # If running part2, look ahead can depend on boxes
                    # if looking up or down, need to look at two squares (if a box)
                    if val == valNew:
                        canMove = self.checkCanMove(d, part2, False, newPos)
                    else:
                        canMoveAhead = True
                        canMoveOffset = True
                        
                        # This is an issue, need to actually run a look ahead (e.g. canMove, because this splits moves one even if the other stops it)
                        if valNew:
                            canMoveAhead = self.checkCanMove(d, part2, False, newPos)
                        if valOffset:
                            canMoveOffset = self.checkCanMove(d, part2, False, offsetNew)
                        
                        canMove = canMoveAhead and canMoveOffset
                
                # Else open space
                else:
                    canMove = True
            
            # If looking left or right, might need to look at an offset position
            else:
                # if looking left
                if d == (-1, 0):
                    # If '[', look at next
                    if val == '[':
                        posToCheck = newPos
                    # Else, look at the offset
                    else:
                        posToCheck = (newPos[0] - 1, newPos[1])
                else:
                    # If ']', look at next
                    if val == ']':
                        posToCheck = newPos
                    # Else, look at the offset
                    else:
                        posToCheck = (newPos[0] + 1, newPos[1])
                    
                checkVal = self.boxes.get(posToCheck, False)
                if posToCheck in self.obstacles:
                    pass
                elif checkVal:
                    canMove = self.checkCanMove(d, part2, False, posToCheck)
                # Else open space
                else:
                    canMove = True
                
        return canMove
    
    # sum the GPS loc of each box (100 * y + x)   
    def getScore(self):
        score = 0
        
        for box, val in self.boxes.items():
            if val == '[' or val == 'O':
                score += 100 * box[1] + box[0]
        
        return score
                
    ## TODO: add widen operation
    def widen(self):
        # Obstacles are now double width (and everything needs to get slid)
        # Boxes are now []
        # newCells = [(oldCellX * 2, oldCellY), (oldCellX * 2 + 1, oldCellY)]
        self.bounds = [self.bounds[0] * 2, self.bounds[1]]
        self.player = (self.player[0] * 2, self.player[1])
        
        newObstacles = set()
        for obstacle in self.obstacles:
            newObstacles.add((obstacle[0] * 2, obstacle[1]))
            newObstacles.add((obstacle[0] * 2 + 1, obstacle[1]))
        self.obstacles = newObstacles
            
        newBoxes = {}
        for box in self.boxes.keys():
            newBoxes[(box[0] * 2, box[1])] = '['
            newBoxes[(box[0] * 2 + 1, box[1])] = ']'
        self.boxes = newBoxes
    
    def __str__(self):
        grid = [['.'] * self.bounds[0] for _ in range(self.bounds[1])]
        grid[self.player[1]][self.player[0]] = '@'
        
        for obstacle in self.obstacles:
            grid[obstacle[1]][obstacle[0]] = '#'
            
        for box, val in self.boxes.items():
            grid[box[1]][box[0]] = val
            
        rowStrs = []
        for row in grid:
            rowStrs.append("".join([str(i) for i in row]))
            
        gridStr = "  \n".join(rowStrs)
        
        return f"{gridStr}\n" #\n  Player: {self.player}\n  Obstacles: {self.obstacles}\n  Boxes: {self.boxes}\n"
        
    def __repr__(self):
        return str(self)
        
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
