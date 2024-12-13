import sys
import os
import regex
import numpy as np

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

# Using regex over re to get branch reset
pattern = regex.compile(r"(?|Button (A|B): X\+(\d*), Y\+(\d*)|(P)rize: X=(\d*), Y=(\d*))")

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    machines = [ClawMachine()]
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip() 
            # Check the line
            m = pattern.match(line)
            if m:
                loc = (int(m.group(2)), int(m.group(3)))
                if m.group(1) == 'A':
                    machines[-1].addA(loc)
                elif m.group(1) == 'B':
                    machines[-1].addB(loc)
                elif m.group(1) == 'P':
                    machines[-1].addPrize(loc)
                    machines.append(ClawMachine())
        
        # Remove the last one (was made as a new one as part of parsing)
        machines.pop()
                    
                    
    for machine in machines:
        score += machine.bruteSolve()
        #print(machine)
    
    # Return Accumulator    
    print(score)
    
    
class ClawMachine:
    def __init__(self):
        self._prize = ()
        self._a = ()
        self._b = ()
        self.init = False
        self.cost = 0
        
    def addA(self, a):
        self._a = a
        if self._b and self._prize:
            self.init = True
        
    def addB(self, b):
        self._b = b
        if self._a and self._prize:
            self.init = True
        
    def addPrize(self, prize):
        self._prize = prize
        if self._a and self._b:
            self.init = True
        
    def __str__(self):
        return f"Machine (init: {self.init}):\n  A: {self._a}\n  B: {self._b}\n  Prize: {self._prize}\n  Cost: {self.cost}\n"
        
    def __repr__(self):
        return str(self)
        
    # Returns the cheapest number of tokens to get the prize, if possible, else 0
    def solve(self):   
        # System of linear equations
        # p.x = A * a.x + B * b.x 
        # p.y = A * a.y + B * b.y
        # Diophantine eqs, want integer solutions 
        rSide = np.array([[self._a[0], self._b[0]], [self._a[1], self._b[1]]])
        lSide = np.array(self._prize)
        sol = np.linalg.solve(rSide, lSide)
        
        self.cost = 0
        
        # Now check if the integer version is valid
        ints = [int(i) for i in sol]
        if all([p == ints[0] * a + ints[1] * b for a, b, p in zip(self._a, self._b, self._prize)]):
            self.cost = ints[0] * 3 + ints[1]
        
        return self.cost
        
    def bruteSolve(self):
        # System of linear equations
        # p.x = A * a.x + B * b.x 
        # p.y = A * a.y + B * b.y
        # Brute forced
        # Worst case cost is 400 (3 * max + max = 4 * max, max = 100)
        self.cost = 401
        for i in range(101):
            for j in range(101):
                if all([p == a * i + b * j for a, b, p in zip(self._a, self._b, self._prize)]):
                    cost = i * 3 + j
                    if cost < self.cost:
                        self.cost = cost
        
        # Clear unsolved max
        self.cost = self.cost if self.cost < 401 else 0
        return self.cost
        
        
    
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
