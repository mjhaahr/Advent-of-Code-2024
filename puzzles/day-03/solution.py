import sys
import re

pattern = re.compile(r"mul\((\d*),(\d*)\)")

def puzzle(filename, part2):
    ops = []
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
                
            ops.extend(pattern.findall(line))
                
    score = 0
    for x, y in ops:
        score += int(x) * int(y)
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
