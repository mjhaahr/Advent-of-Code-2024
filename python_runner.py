#!/usr/bin/env python

# Runs a given days code
import sys
import os


## Expected Input Setup:
# [day#], [part# = {1,2}], [dataSet = 0 (0 for true input, 1+ for examples 1+)]

if __name__ == "__main__":
    day = 0
    part2 = False
    dataSet = 0
    
    match len(sys.argv):
        case 2:
            day = int(sys.argv[1])
        
        case 3:
            day = int(sys.argv[1])
            part2 = sys.argv[2] == '2'
        
        case 4:
            day = int(sys.argv[1])
            part2 = sys.argv[2] == '2'
            dataSet = int(sys.argv[3])
            
        case _:
            print(f"Error: Expected 1-3 arguments, got {len(sys.argv) - 1}")
            exit()
    
    inputName = "input"
    if (dataSet > 0):
        inputName = f"example{dataSet}"
    
    print(f"Running Day-{day:02d} Part {'2' if (part2 == True) else '1'} with {inputName}.txt")
    path = f"./python/puzzles/day-{day:02d}/solution.py"
    inputPath = f"./inputs/day-{day:02d}/{inputName}.txt"
    
    os.system(f"python {path} {inputPath} {'2' if (part2 == True) else '1'}")
