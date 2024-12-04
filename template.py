import sys
import os

# setting path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))

# importing
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    # Open File
    with open(filename, 'r') as fp:
        while True:
            # Loop over all lines
            line = fp.readline()
            
            # EOF check
            if line == '':
                break   
    
    # Return Accumulator    
    print(score)
    

        
l = [['1', '2'], ['3', '4']]

g = utils.Grid(l)
print(g)
print(g.get(0, 0))
print(g.get((1, 1)))
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
