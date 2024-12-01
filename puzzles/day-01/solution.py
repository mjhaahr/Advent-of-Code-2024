import sys

def puzzle(filename, part2):
    list0 = []
    list1 = []
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
                
            lineData = line.split()
            
            list0.append(int(lineData[0]))
            list1.append(int(lineData[1]))
       
    score = 0
    for x, y in zip(sorted(list0), sorted(list1)):
        score += abs(x - y)
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
