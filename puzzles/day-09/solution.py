import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    # Open File
    with open(filename, 'r') as fp:
        # only one line today
        line = fp.readline().strip()
        
    disk = []
    # Loop over all characters and add their length to the list as appropriate
    for idx, block in enumerate(line):
        blockLen = int(block)
        # File Entry
        if idx % 2 == 0:
            blockId = idx // 2
            entry = [blockId]
        # Free Entry
        else:
            entry = ['.']
            
        disk.extend(entry * blockLen)
    
    # Disk compression
    nextFree = 0
    lastFilled = len(disk) - 1
    while True:
            
        # Find first free slot (if the current one is not free)
        while disk[nextFree] != '.':
            nextFree += 1
        
        # Find last filled slot (if the current one is free)
        while disk[lastFilled] == '.':
            lastFilled -= 1
            
        # If the disk is compressed, stop
        if lastFilled < nextFree:
            break
                
        disk[nextFree] = disk[lastFilled]
        disk[lastFilled] = '.'
    
    # Calculate the check sum
    for i, d in enumerate(disk):
        if d == '.':
            break
        
        score += i * d
        
    # Return Accumulator    
    print(score)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
