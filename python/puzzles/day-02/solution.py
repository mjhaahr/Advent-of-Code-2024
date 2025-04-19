import sys
from copy import deepcopy as copy

def puzzle(filename, part2):
    reports = []
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
                
            reports.append(list(int(i) for i in line.split()))
            
    score = 0
    for num, report in enumerate(reports):
        res = parseReport(report)
        
        if res == -1:
            score += 1
        elif part2 == True:
            for i in range(res - 1, res + 2):
                newReport = copy(report)
                newReport.pop(i)
                
                if parseReport(newReport) == -1:
                    score += 1
                    break
            
    print(score)
   
# Returns -1 if valid, else returns index of error
def parseReport(report):
    errorIdx = -1
    first = True
    isIncr = True
    
    for idx, (level1, level2) in enumerate(zip(report, report[1:])):
        delta = level1 - level2
        diff = abs(delta)
        if diff < 1 or diff > 3:
            errorIdx = idx
            break
        
        currIncr = delta > 0
        if first:
            isIncr = currIncr
            first = False
        elif currIncr != isIncr:
            errorIdx = idx
            break
            
    return errorIdx
    
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
