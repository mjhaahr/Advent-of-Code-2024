import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils
    
# Right Rules, key is left value, value is list of right values that must come after
rightRules = {}
# Right Rules, key is right value, value is list of left values that must come before
leftRules = {}

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    updates = []
    
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
                    updates.append(list(int(i) for i in line.split(',')))
                    
            except IndexError:
                continue
    
    # Loop over orders
    for upd in updates:
        # Loop over elements
        goodUpdate = True
        for i, val in enumerate(upd):
            # Check right values
            rightRule = rightRules.get(val, [])
            # For each in the right-ward values of the list, check if it's in rightRule
            goodRight = all([(j in rightRule) for j in upd[(i + 1):]])
            
            # Check left values
            leftRule = leftRules.get(val, [])
            # For each in the left-ward values of the list, check if it's in leftRule
            goodLeft = all([(j in leftRule) for j in upd[:(i)]])
            
            # If one is bad, exit
            if not goodLeft or not goodRight:
                goodUpdate = False
                break
        
        if part2 is False:
            # if a good update, take center of list and add to sum  
            if goodUpdate:
                score += upd[len(upd)//2]
        # if Part 2, re-sort the bad orders then add center
        else:
            if not goodUpdate:
                newUpdate = resortUpdate(upd)
                score += newUpdate[len(newUpdate)//2]
            
            
    
    # Return Accumulator    
    print(score)
    
def resortUpdate(upd):
    newUpdate = [upd[0]]
    
    for page in upd[1:]:
        leftRule = leftRules.get(page, [])
        rightRule = rightRules.get(page, [])
        added = False
        for i, val in enumerate(newUpdate):
            # If the value is not in the left rule, means that's the furthest it can go
            if val not in leftRule:
                newUpdate.insert(i, page)
                added = True
                break
        
        if not added:
            newUpdate.append(page)
    
    return newUpdate
    
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
