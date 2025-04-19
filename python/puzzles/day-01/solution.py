import sys

def puzzle(filename, part2):
    list0 = []
    list1 = []
    list1D = {}
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
                
            lineData = line.split()
            
            list0Data = int(lineData[0])            
            list1Data = int(lineData[1])
            
            list0.append(list0Data)
            list1.append(list1Data)
            list1D[list1Data] = list1D.get(list1Data, 0) + 1
            
       
    score = 0
    
    if part2 == False:
        for x, y in zip(sorted(list0), sorted(list1)):
            score += abs(x - y)
    else:
        for x in list0:
            freq = list1D.get(x, 0)
            score += x * freq
        
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
