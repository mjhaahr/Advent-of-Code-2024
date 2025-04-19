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
        bases = fp.readline().strip().split(', ')
        fp.readline()
        targets = []
        for line in fp.readlines():
            line = line.strip() 
            targets.append(line)
            if len(line) > maxLen:
                maxLen = len(line)
    
    cache = {}
    
    for num, target in enumerate(targets):
        out = composable(target, bases, cache)
        if not part2:
            score += 1 if out > 0 else 0
        else:
            score += out
        
        
    # Return Accumulator    
    print(score)
    

# Recursively search through the beginning of words 
def composable(target, bases, cache):
    # If empty, return 1, one way to compose
    if target == "":
        return 1 
        
    # If already seen, return that
    if target in cache:
        return cache[target]
        
    # Assume 0 if not seen it
    ways = 0
        
    # For all the substrings
    for base in bases:
        # If the start is equal, store number of ways it's composable
        if target.startswith(base):
            ways += composable(target[len(base):], bases, cache)
    
    # Update storage
    cache[target] = ways
    # Return the found value
    return ways  
        
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
