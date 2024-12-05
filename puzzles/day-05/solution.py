import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    # Right Rules, key is left value, value is list of right values that must come after
    rightRules = {}
    # Right Rules, key is right value, value is list of left values that must come before
    leftRules = {}
    
    orders = []
    
    # Open File
    with open(filename, 'r') as fp:
        while True:
            # Loop over all lines
            line = fp.readline()
            
            try:
                # EOF check
                if line == '':
                    break   
                    
                # Process Rule  
                elif line[2] == '|':
                    splits = line.split('|')
                    lVal = int(splits[0])
                    rVal = int(splits[1])
                    
                    rightRule = rightRules.get(lVal, [])
                    rightRule.append(rVal)
                    rightRules[lVal] = rightRule
                    
                    leftRule = leftRules.get(rVal, [])
                    leftRule.append(lVal) 
                    leftRules[rVal] = leftRule
                    
                # Process Order
                elif line[2] == ',':
                    orders.append(list(int(i) for i in line.split(',')))
                    
            except IndexError:
                continue
    
    # Loop over orders
    for order in orders:
        # Loop over elements
        goodOrder = True
        for i, val in enumerate(order):
            # Check right values
            rightRule = rightRules.get(val, [])
            # For each in the right-ward values of the list, check if it's in rightRule
            goodRight = all([(j in rightRule) for j in order[(i + 1):]])
            
            # Check left values
            leftRule = leftRules.get(val, [])
            # For each in the left-ward values of the list, check if it's in leftRule
            goodLeft = all([(j in leftRule) for j in order[:(i)]])
            
            # If one is bad, exit
            if not goodLeft or not goodRight:
                goodOrder = False
                break
        
        # if a good order, take center of list and add to sum  
        if goodOrder:
            score += order[len(order)//2]
    
    # Return Accumulator    
    print(score)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
