#!/usr/bin/env python
import os
import re

pattern = re.compile(r"example(\d*)")

days = sorted(os.listdir("inputs"))
dir = f"inputs/{days[-1]}"
print(dir)

print("Would you like to add the input file or another example?\nEnter I[nput]/i[nput] for input or E[xample]/e[xample] for example")
res = input().lower()
if res == 'i':
    file = f"{dir}/input.txt"
    print(f"\nThis will create/modify: {file}\nPress Y/y to accept:")
    res = input().lower()
    if res == 'y':
        os.system(f"nano {file}")
        
elif res == 'e':
    largestEx = 0
    for file in os.listdir(dir):
        m = pattern.search(file)
        if m:
            newNum = int(m.group(1))
        
            if newNum > largestEx:
                largestEx = newNum
    
    file = f"{dir}/example{largestEx + 1}.txt"
        
    print(f"\nThis will create: {file}\nPress Y/y to accept:")
    res = input().lower()
    if res == 'y':
        os.system(f"nano {file}")
        
    
    