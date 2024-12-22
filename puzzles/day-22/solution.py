import sys
import os

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0

    numbers = []

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip()
            numbers.append(int(line))

    for number in numbers:
        score += calcSecret(number, 2000)

    # Return Accumulator
    print(score)

def calcSecret(num, iters):
    for i in range(iters):
        num = mix(num * 64, num)
        num = prune(num)

        num = mix(num // 32, num)
        num = prune(num)

        num = mix(num * 2048, num)
        num = prune(num)

    return num

def mix(num, secret):
    return num ^ secret

def prune(num):
    return num % 16777216

if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
