import sys

def puzzle(filename, part2):
    reports = []
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
                
            reports.append(list(int(i) for i in line.split()))
            
    score = 0
    for levels in reports:
        incr = (levels[1] > levels[0])
        valid = True
        for level1, level2 in zip(levels, levels[1:]):
            diff = abs(level1 - level2)
            currIncr = level2 > level1
            
            if diff < 1 or diff > 3:
                valid = False
                break
            elif currIncr != incr:
                valid = False
                break
                
        score += 1 if valid else 0
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
