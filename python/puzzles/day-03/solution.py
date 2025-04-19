import sys
import re

# Find the multiplication and control instructions
pattern = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")

def puzzle(filename, part2):
    # Start enabled
    enable = True
    # Accumulator
    score = 0
    
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
            
            # Loop over all the found instructions
            for inst in pattern.finditer(line):
                if inst.group(0) == "do()":
                    # "do()" enables the following instructions until the next "don't()"
                    # Does not affect Part 1
                    enable = True
                elif inst.group(0) == "don't()":
                    # "don't()" disables the following instructions until the next "do()"
                    # If running Part 1, force set enable to true to ignore the control instructions
                    enable = False if (part2 == True) else True
                elif enable:
                    # if enabled, perform the multiplication instruction
                    score += int(inst.group(1)) * int(inst.group(2))
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
