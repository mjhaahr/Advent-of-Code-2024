import sys
import os

# setting path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

# importing
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
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
                   
            strs.append(list(c for c in line if c.isalpha()))
            
    wordsearch = utils.Grid(strs)
       
    # Look for 'X' then run DFS around it and continue in that direction
    for y, row in enumerate(wordsearch):
        for x, char in enumerate(row):
            if part2 == False:
                # If found 'X', could be the start of an 'XMAS'
                if char == 'X':
                    score += findXMAS(x, y, wordsearch)
            else:
                # If running Part2, looking for 'A'
                if char == 'A':
                    score += findMAS(x, y, wordsearch)
        
    print(score)

# Takes a positon (at an 'X') and looks for 'XMAS' around it    
# Returns the number of valid XMAS's
def findXMAS(x, y, wordsearch):
    xmases = 0
    if wordsearch.get(x, y) == 'X':
        # Loop over alternate directions to find the surroundings
        for val, newX, newY, i, j in wordsearch.getNeighborsOf8(x, y):
            if val == 'M':
                xmases += digInDir(newX, newY, i, j, 'A', wordsearch)
                
    return xmases
   
# digs in a direction (recursion) to find the rest of XMAS 
def digInDir(x, y, i, j, target, wordsearch):
    newX = x + i
    newY = y + j
    if wordsearch.get(newX, newY) == target:
        # Found target, time to find next
        if target == 'A':
            return digInDir(newX, newY, i, j, 'S', wordsearch)
        # Found XMAS
        elif target == 'S':
            return 1
    else:
        return 0
    
# Tries to find if the current A is located in an X
def findMAS(x, y, wordsearch):
    valid = 0
    # If not actually an 'A', skip
    if wordsearch.get(x, y) != 'A':
        pass
    else:
        # Get the chars of interest
        COI = wordsearch.getNeighborsOf4Rot(x, y)
        [UL, UR, DL, DR] = [i[0] for i in COI]
        
        # Check first diagonal
        if (UL == 'M' and DR == 'S') or (UL == 'S' and DR == 'M'):
            # Check Second Diagonal
            if (UR == 'M' and DL == 'S') or (UR == 'S' and DL == 'M'):
                valid = 1
                
                
    return valid
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
