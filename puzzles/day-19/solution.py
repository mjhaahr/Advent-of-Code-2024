import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    maxLen = 0
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        bases = fp.readline().split(', ')
        fp.readline()
        targets = []
        for line in fp.readlines():
            line = line.strip() 
            targets.append(line)
            if len(line) > maxLen:
                maxLen = len(line)
    
    cache = {}
    
    for num, target in enumerate(targets):
        print(f"Progress: {num}/{len(targets)}, curr score: {score}")
        if composable(target, bases, cache):
            score += 1
        
        
    # Return Accumulator    
    print(score)
    

# Recursively search through the beginning of words 
def composable(target, bases, cache):
    # If empty, return true
    if target == "":
        return True 
        
    # If already seen, return that
    if target in cache:
        return cache[target]
        
    # Assume False if not seen it
    cache[target] = False
        
    # For all the substrings
    for base in bases:
            
        length = len(base)
        # Break into start and rest
        start = target[0:length]
        rest = target[length:]
        
        # If the start is equal AND the if the rest is composable, store true (and break), else continue
        if start == base and composable(rest, bases, cache):
            cache[target] = True
            break
    
    # Return the found value
    return cache[target]   
        
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
