import sys

def puzzle(filename, part2):
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if line == '':
                break   
        
    score = 0
    print(score)
    
if __name__ == "__main__":
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
