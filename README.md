# Advent of Code 2024

Repo for my entries for [Advent of Code 2024](https://adventofcode.com/2024/about). 

All are solved in vanilla Python (using lots of `itertools` and `re`/`regex` as well as the occasional `heapq` and `functools`)

## Usage

To run, use the provided `runner.py` script:

```
python runner.py [day#] [part# = 1] [dataSet = 0]
# day#: Sets the day to run
# part#: Sets which part to run (defaults to 1 unless 2 is entered)
# dataSet: Which data set to use, 0 (or any negative) is puzzle input, 1+ is for examples 1+
# data sets are stored in the inputs/day-# dir
```

Each day uses a common utilities module (called `utils.py`), mostly for graph and traversal utilies, this stays in the top-level-directory for the repo, and is included using some path management shenanigans

To create a new day, use the provided `makeday.py` script, which will create the puzzle and input file directories and creates (and optionally opens) the `solution.py` script.

To add an input to the most recent day, use the provided `addinput.py` script, which asks whether you'd like to add the input file or an example file and then opens it with `nano`

_All the helpful scripts (`runner.py`, `makeday.py`, and `addinput.py`) are a little silly and abuse the `os` and `sys` modules_ 
