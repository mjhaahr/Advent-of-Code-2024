import sys
import re

# Find just the multiplication instructions
part1Pattern = re.compile(r"mul\((\d*),(\d*)\)")
# Find the multiplication and control instructions
part2Pattern = re.compile(r"mul\((\d*),(\d*)\)|do\(\)|don't\(\)")

def puzzle(filename, part2):
    instructions = []
    # Start enabled
    enable = True
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
            
            if part2 == False:
                # Add the new instructions to the list
                instructions.extend(part1Pattern.findall(line))
            else:
                # Loop over all the found instructions
                for inst in part2Pattern.finditer(line):
                    if inst.group(0) == "do()":
                        # "do()" enables the following instructions until the next "don't()"
                        enable = True
                    elif inst.group(0) == "don't()":
                        # "don't()" disables the following instructions until the next "do()"
                        enable = False
                    elif enable:
                        # if enabled, store the standard multiplication instruction
                        instructions.append([inst.group(1), inst.group(2)])
    
    score = 0
    # Perform the multiplication instructions and sum
    for x, y in instructions:
        score += int(x) * int(y)
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
