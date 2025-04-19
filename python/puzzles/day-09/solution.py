import sys
import os
from itertools import islice

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
    if not part2:
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
    else:
        # [startAddress of lastFilled, endAddress of lastFilled]
        lastFilled = [len(disk) - 1, len(disk) - 1]
        firstFree = int(line[0])
        seenBlocks = set()
        while True:
            # Find last filled slot (if the current one is free)
            while disk[lastFilled[1]] == '.':
                lastFilled[1] -= 1
            
            blockId = disk[lastFilled[1]]
               
            # End of compression, all filled
            if firstFree > lastFilled[1]:
                break
            
            lastFilled[0] = lastFilled[1]
            # Find beginning of the lastFilled
            while disk[lastFilled[0]] == blockId:
                lastFilled[0] -= 1
            
            # restore over subtraction
            lastFilled[0] += 1
            
            # End of compression, all filled
            if firstFree > lastFilled[0]:
                break
            
            # skip already seen blocks, look for next
            if blockId in seenBlocks:
                lastFilled[1] = lastFilled[0] - 1
                continue
            else:
                seenBlocks.add(blockId)
            
            print(f"{blockId} @ {lastFilled[1]}  FF @ {firstFree}: {disk[firstFree]}")
            
            blockLen = (lastFilled[1] - lastFilled[0]) + 1
            
            freeLoc = findFreeSlot(firstFree, lastFilled[0], blockLen, disk)
            # Could not find appropriate window, look for next
            if freeLoc < 0:
                lastFilled[1] = lastFilled[0] - 1
                continue
            # Not productive to move to this free slot
            elif freeLoc > lastFilled[0]:
                lastFilled[1] = lastFilled[0] - 1
                continue
                
            for i in range(freeLoc, freeLoc + blockLen):
                disk[i] = blockId
            
            for i in range(lastFilled[0], lastFilled[1] + 1):
                disk[i] = '.'
                
            # Move the pointer to the first free block if the freeLoc is on top of the first free
            if freeLoc == firstFree:
                # Search for next free, starting at the end of the prior block
                firstFree = freeLoc + blockLen
                while disk[firstFree] != '.':
                    firstFree += 1
    
    # Calculate the check sum
    for i, d in enumerate(disk):
        if d == '.':
            continue
    
        score += i * d
        
    # Return Accumulator    
    print(score)
    
    
def findFreeSlot(firstFree, maxIdx, n, disk):
    idx = firstFree
    while True:
        if idx > maxIdx:
            return -1
            
        window = list(islice(disk, idx, idx + n))
        if all([s == '.' for s in window]):
            return idx
        else:
            toSkip = n
            while True:
                lastVal = window.pop()
                if lastVal != '.':
                    break
                toSkip -= 1
                
            idx += toSkip
        
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
