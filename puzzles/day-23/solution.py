import sys
import os
import re
from collections import defaultdict
from itertools import combinations

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0

    connections = defaultdict(set)

    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            line = line.strip()
            a = line[0:2]
            b = line[3:5]
            connections[a].add(b)
            connections[b].add(a)

    # Sets of tuples (sort alphabetically)
    games = set()

    if not part2:
        for a, connectsTo in connections.items():
            # For each combination of 2 elements of connectsTo, check if both connect to each other
            for b, c in combinations(connectsTo, 2):
                if c in connections[b]:
                    newGame = tuple(sorted([a, b, c]))
                    games.add(newGame)

        for game in games:
            for comp in game:
                if comp[0] == 't':
                    score += 1
                    break

    else:
        for a, connectsTo in connections.items():
            # For each combination of 2 elements of connectsTo, check if both connect to each other
            for i in range(2, len(connectsTo)):
                for combo in combinations(connectsTo, i):
                    found = True
                    for comp in combo:
                        for other in combo:
                            if comp == other:
                                continue
                            elif other not in connections[comp]:
                                found = False
                                break

                        if not found:
                            break

                    if found:
                        l = list(combo)
                        l.append(a)
                        newGame = tuple(sorted(l))
                        games.add(newGame)

        print(*max(games, key=len), sep=',')

    # Return Accumulator
    print(score)

if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")

    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
