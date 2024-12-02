#!/usr/bin/env python
import os

days = sorted(os.listdir("puzzles"))

day = int(days[-1].split('-')[-1]) + 1

dayName = f"day-{day:02d}"
puzzleEntry = f"puzzles/{dayName}"
solEntry = f"{puzzleEntry}/solution.py"
inputsEntry = f"inputs/{dayName}"

print(f"Do you want to create:\n{' '*4}{puzzleEntry}\n{' '*4}{solEntry}\n{' '*4}{inputsEntry}\n\nPress Y/y to accept:")

res = input()
if res.lower() == 'y':
    os.system(f"mkdir -p {puzzleEntry}")
    os.system(f"mkdir -p {inputsEntry}")
    os.system(f"cp -p ./template.py {solEntry}")
    print("\nWould you like to open the new solution script\nPress Y/y to accept:")
    
    res = input()
    if res.lower() == 'y':
        os.system(f"open {solEntry}")
