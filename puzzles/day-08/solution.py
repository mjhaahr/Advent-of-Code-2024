import sys
import os
from itertools import combinations

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    bounds = [0, 0]
    freqs = {}
    
    # Algo:
    # Find all nodes
    # Loop over all frequencies to create pairs of nodes
    # If the anti-nodes for that pair are in the bounds, add to a set
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        line = fp.readline()
        y = 0
        while line:
            bounds[1] = y
            
            for x, char in enumerate(line.strip()):
                if x > bounds[0]:
                    bounds[0] = x
                if char != '.':
                    nodes = freqs.get(char, [])
                    nodes.append([x, y])
                    freqs[char] = nodes
            
            line = fp.readline() 
            y += 1
    
    antinodes = set()
    
    for freq, nodes in freqs.items():
        for a, b in combinations(nodes, 2):
            distX = a[0] - b[0]
            distY = a[1] - b[1]
            dist = [distX, distY]
            
            a1 = [i + j for i, j in zip(a, dist)]
            a2 = [i - j for i, j in zip(b, dist)]
            
            for x, y in [a1, a2]:
                if x >= 0 and y >= 0 and x <= bounds[0] and y <= bounds[1]:
                    antinodes.add(tuple([x, y]))
            
    score = len(antinodes)
        
    # Return Accumulator    
    print(score)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
