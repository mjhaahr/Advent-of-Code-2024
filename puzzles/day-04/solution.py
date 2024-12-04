import sys
    
# Create grid of letters
wordsearch = []
dims = [0, 0]

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    global wordsearch
    
    # Open File
    with open(filename, 'r') as fp:
        while True:
            # Loop over all lines
            line = fp.readline()
            
            # EOF check
            if line == '':
                break   
                   
            wordsearch.append(list(c for c in line if c.isalpha()))
            
    dims[1] = len(wordsearch) - 1
    dims[0] = len(wordsearch[0]) - 1
       
    # Look for 'X' then run DFS around it and continue in that direction
    for y, row in enumerate(wordsearch):
        for x, char in enumerate(row):
            if part2 == False:
                # If found 'X', could be the start of an 'XMAS'
                if char == 'X':
                    score += findXMAS(x, y)
            else:
                # If running Part2, looking for 'A'
                if char == 'A':
                    score += findMAS(x, y)
        
    print(score)

# Takes a positon (at an 'X') and looks for 'XMAS' around it    
# Returns the number of valid XMAS's
def findXMAS(x, y):
    xmases = 0
    if wordsearch[y][x] == 'X':
        # Loop over alternate directions to find the surroundings
        for j in [-1, 0, 1]:
            for i in [-1, 0, 1]:
                # If at the center, skip
                if i == 0 and j == 0:
                    continue
                    
                xmases += digInDir(x, y, i, j, 'M')
                
    return xmases
   
# digs in a direction (recursion) to find the rest of XMAS 
def digInDir(x, y, i, j, target):
    newX = x + i
    newY = y + j
    # If at a bounds, exit early
    if newX < 0 or newY < 0 or newX > dims[0] or newY > dims[1]:
        return 0
    # Found target, time to find next
    elif wordsearch[newY][newX] == target:
        if target == 'M':
            return digInDir(newX, newY, i, j, 'A')
        elif target == 'A':
            return digInDir(newX, newY, i, j, 'S')
        # Found XMAS
        elif target == 'S':
            return 1
    else:
        return 0
    
# Tries to find if the current A is located in an X
def findMAS(x, y):
    valid = 0
    # If not actually an 'A', skip
    if wordsearch[y][x] != 'A':
        pass
    # If at a bounds, skip, cannot be valid there
    if x <= 0 or y <= 0 or x >= dims[0] or y >= dims[1]:
        pass
    else:
        # Get the chars of interest
        UL = wordsearch[y - 1][x - 1]
        UR = wordsearch[y - 1][x + 1]
        DL = wordsearch[y + 1][x - 1]
        DR = wordsearch[y + 1][x + 1]
        
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
