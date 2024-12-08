import sys
import os
import re
from itertools import product
import copy

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

pattern = re.compile(r"(\d*): (.*)")

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    eqs = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        line = fp.readline()
        while line:
            m = pattern.match(line)
            
            val = int(m.group(1))
            comps = list(int(i) for i in m.group(2).split())
            
            eqs.append([val, comps])
            
            line = fp.readline()  
    
    for eq in eqs:
        val = eq[0]
        comps = eq[1]
        for ops in product(['+', '*'], repeat = (len(comps) - 1)):
            if performOp(copy.copy(comps), list(ops)) == val:
                score += val
                break
            
        
    # Return Accumulator    
    print(score)
    
    
def performOp(listOfVals, listOfOps):
    # Empty list, return value
    val = listOfVals.pop(0)
    if not listOfOps:
        return val
        
    op = listOfOps.pop(0)
    match op:
        case '+':
            listOfVals[0] = val + listOfVals[0]
    
        case '*':
            listOfVals[0] = val * listOfVals[0]
            
    return performOp(listOfVals, listOfOps)
    
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
