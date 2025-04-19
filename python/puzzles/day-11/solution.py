import sys
import os
from collections import defaultdict

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    # Open File
    with open(filename, 'r') as fp:
        # Split the stones out
        stones = defaultdict(int)
        for stone in [int(i) for i in fp.readline().strip().split()]:
            stones[stone] += 1
        
    num = 75 if part2 else 25
    for i in range(num):
        stones = runBlink(stones)
    
    score = sum(stones.values())
    
    # Return Accumulator    
    print(score)
  

# Stones the number of each stone type in a dict
def runBlink(stones):
    newStones = defaultdict(int)
    
    for stone, num in stones.items():
        stoneAsStr = str(stone)
        lenStone = len(stoneAsStr)
        
        if stone == 0:
            newStones[1] += num
        elif lenStone % 2 == 0:
            midpoint = lenStone // 2
            newStones[int(stoneAsStr[midpoint:])] += num
            newStones[int(stoneAsStr[:midpoint])] += num
        else:
            newStones[stone*2024] += num
    
    return newStones
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
