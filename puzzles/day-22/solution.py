import sys
import os
from collections import deque, defaultdict

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

    if not part2:
        for num in numbers:
            score += runSecrets(num, 2000)
    else:
        score = findBestSequence(numbers, 2000)


    # Return Accumulator
    print(score)


def runSecrets(num, iters):
    for i in range(iters):
        num = calcSecret(num)

    return num


def findBestSequence(numbers, iters):
    results = []
    sequenceScores = defaultdict(lambda: 0)
    for num in numbers:
        results = findPrices(num, iters)

        for sequence, score in findSequenceScores(results).items():
            sequenceScores[sequence] += score

    return max(sequenceScores.values())


def findSequenceScores(prices):
    sequenceScores = defaultdict(lambda: 0)
    for p, s in prices:
        if s not in sequenceScores:
            sequenceScores[s] = p

    return sequenceScores


def findPrices(num, iters):
    price = num % 10

    results = []
    sequence = deque()

    for i in range(iters):
        num = calcSecret(num)
        newPrice = num % 10
        delta = newPrice - price
        price = newPrice
        sequence.append(delta)
        if len(sequence) == 4:
            results.append((price, tuple(sequence)))
            sequence.popleft()

    return results


def calcSecret(num):
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
