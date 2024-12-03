import sys
import re

# Find just the multiplication instructions
part1Pattern = re.compile(r"mul\((\d*),(\d*)\)")
# Find the multiplication and control instructions
part2Pattern = re.compile(r"mul\((\d*),(\d*)\)|do\(\)|don't\(\)")

def puzzle(filename, part2):
    instructions = []
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
                        # "do()" enables the multiplication
                        instructions.append(True)
                    elif inst.group(0) == "don't()":
                        # "don't()" disables the multiplication
                        instructions.append(False)
                    else:
                        # else just store the standard multiplication operation
                        instructions.append([inst.group(1), inst.group(2)])           
    
    # If part 2, filter out the disabled instructions
    if part2:
        # Start enabled
        enable = True
        filteredInstructions = []
        # Loop over all instructions
        for inst in instructions:
            if type(inst) == bool:
                # If the instruction is a control type, update the enable flag accordingly
                enable = inst
            elif enable:
                # If the instruction is not a control inst (must be multiplication) AND they are enabled, add to the new list
                filteredInstructions.append(inst)
                
        instructions = filteredInstructions
    
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
