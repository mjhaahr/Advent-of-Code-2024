import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

debug = False

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    cpu = Computer()
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip() 
            
            splits = line.split()
            if "Register" in line:
                cpu.addReg(splits[1][0], int(splits[2]))
            elif "Program" in line:
                args = splits[1].split(',')
                for opcode, operand in zip(args[::2], args[1::2]):
                    cpu.addOp(int(opcode), int(operand))
    if debug:
        print(cpu)
        
    score = cpu.runProg()
    
    # Return Accumulator    
    print(score)
    
class Computer:
    def __init__(self):
        self.A = 0
        self.B = 0
        self.C = 0
        self.prog = []
        self.output = []
        
    def addReg(self, reg, val):
        match reg:
            case 'A':
                self.A = val
            case 'B':
                self.B = val
            case 'C':
                self.C = val
                
    def addOp(self, opcode, operand):
        self.prog.append((opcode, operand))
        
    def runProg(self):
        # Loop until PC overruns length
        pc = 0
        while pc < len(self.prog):
           pc = self.executeInst(pc)
           
        return ','.join(self.output)
           
    # Returns the updated PC
    def executeInst(self, pc):
        opcode, operand = self.prog[pc]
        if debug:
            print(f"PC: {pc}: {opcode}, {operand}")
            
        newPC = pc + 1
        
        match opcode:
            case 0:
                div = 2 ** self.getCombo(operand)
                out = self.A // div
                if debug:
                    print(f"  adv: A({self.A}) / c({operand})({div}) = {out}")
                self.A = out
                
            case 1:
                out = self.B ^ operand
                if debug:
                    print(f"  bxl: B({self.B}) ^ l({operand}) = {out}")
                self.B = out
                
            case 2:
                out = self.getCombo(operand) % 8
                if debug:
                    print(f"  bst: c({operand})({self.getCombo(operand)}) % 8 = {out}")
                self.B = out
                
            case 3:
                if self.A != 0:
                    newPC = operand
                    if newPC == pc:
                        newPC += 2
                if debug:
                    print(f"  jnz: New PC: {newPC}, Jump {'Not ' if self.A == 0 else ''}Taken")
            
            case 4:
                out = self.B ^ self.C
                if debug:
                    print(f"  bxc: B({self.B}) % ^ C({self.C}) = {out}")
                self.B = out
                
            case 5:
                out = self.getCombo(operand) % 8
                if debug:
                    print(f"  out: c({operand})({self.getCombo(operand)}) % 8 = {out}")
                self.output.append(str(out))
                
            case 6:
                div = 2 ** self.getCombo(operand)
                out = self.A // div
                if debug:
                    print(f"  bdv: {self.A} / {div} = {out}")
                self.B = out
            
            case 7:
                div = 2 ** self.getCombo(operand)
                out = self.A // div
                if debug:
                    print(f"  cdv: {self.A} / {div} = {out}")
                self.C = out
                
        if debug:
            print(self)
        
        return newPC
        
        
    def getCombo(self, val):
        out = val
        match val:
            case 4:
                out = self.A
            case 5:
                out = self.B
            case 6:
                out = self.C
            
        return out
        
        
    def __str__(self):
        return f"Computer:\n  Reg A: {self.A}\n  Reg B: {self.B}\n  Reg C: {self.C}\n  Ops: {self.prog}\n  Out: {self.output}\n"
        
    def __repr__(self):
        return str(self)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
