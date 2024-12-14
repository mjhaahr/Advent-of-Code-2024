import sys
import os
import re
from math import ceil, floor 
from time import sleep

pattern = re.compile(r"p=(\d+),(\d+) v=(-?\d+),(-?\d+)")

# Modifying Path to include Repo Directory (for util import)
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))))
# Import Utilities
import utils

def puzzle(filename, part2):
    # Zero the Accumulator
    score = 0
    
    robots = []
    
    # Open File
    with open(filename, 'r') as fp:
        # Loop over all lines
        for line in fp.readlines():
            m = pattern.match(line)
            if m:
                robots.append(Robot(int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
    
    # Setup the world bounds
    if "example" in filename:
        world = [11, 7]
    else:
        world = [101, 103]
        
    if not part2:
    
        # Move each robot 100 times
        for robot in robots:
            robot.moveNTimes(world, 100)
        
        halfX = world[0] / 2
        halfY = world[1] / 2
    
        quadrants = [[0, 0, floor(halfX) - 1, floor(halfY) - 1],
                        [0, ceil(halfY), floor(halfX) - 1, world[1] - 1],
                        [ceil(halfX), 0, world[0] - 1, floor(halfY) - 1],
                        [ceil(halfX), ceil(halfY), world[0] - 1, world[1] - 1]]
        inQuad = [0] * 4
    
        for robot in robots:
            for i, quad in enumerate(quadrants):
                if robot.isWithin(quad):
                    inQuad[i] += 1
                    break
        
        score = 1
        for i in inQuad:
            score *= i    
    else:
        # Find number of iterations to make a christmas tree?
        # Set to False for animation (tree occurs at frame: )
        if True:
            exit = False
            
            while True:
                poses = set()
                for robot in robots:
                    robot.moveNTimes(world, score)
                    poses.add(robot.p)
                
                """   
                # All robots at unique locations
                if len(poses) == len(robots):
                    break
                """
                
                if score % 100 == 0:
                    print(score)
                
                # Found line in the space
                for line in makeGrid(world, robots):
                    if "■■■■■■■■■■■■" in line:
                        exit = True
                        break
                    
                if exit:
                    break
                    
                score += 1
                
                    
                
        else:
            animate(world, robots, 0, 100)
            
    
    # Return Accumulator    
    print(score)

def animate(world, robots, startFrame, endFrame, stride = 1):
    frame = startFrame
    while frame <= endFrame:
        # Gen frame data
        for robot in robots:
            robot.moveNTimes(world, frame)
        
        # Clear the screen
        os.system('cls' if os.name == 'nt' else 'clear')
        # "Draw" the screen
        print(*makeGrid(world, robots), sep='\n')
        print("\n\n\n ")
        # Iterate
        frame += stride
        # Sleep
        sleep(1)
    
    
def makeGrid(world, robots):
    grid = [[' '] * world[0] for _ in range(world[1])]
    
    for robot in robots:
        grid[robot.p[1]][robot.p[0]] = '■'
    
    for i, line in enumerate(grid):
        string = ''.join(line)
        grid[i] = string
    
    return grid
    
class Robot:
    def __init__(self, x, y, vx, vy):
        self.p = (x, y)
        self.v = (vx, vy)
        
    def move(self, bounds):
        newX = (self.p[0] + self.v[0]) % bounds[0]
        newY = (self.p[1] + self.v[1]) % bounds[1]
        self.p = (newX, newY)
        
    def moveNTimes(self, bounds, n):
        newX = (self.p[0] + self.v[0] * n) % bounds[0]
        newY = (self.p[1] + self.v[1] * n) % bounds[1]
            
        self.p = (newX, newY)
       
    # Expects bounds x0, y0, x1, y1 
    def isWithin(self, bounds):
        if self.p[0] < bounds[0] or self.p[1] < bounds[1] or self.p[0] > bounds[2] or self.p[1] > bounds[3]:
            return False
        else:
            return True
        
    def __str__(self):
        return f"Robot @ {self.p} going {self.v}"
        
    def __repr__(self):
        return str(self)
    
if __name__ == "__main__":
    # Check number of Arguments, expect 2 (after script itself)
    # Args: input file, part number
    if (len(sys.argv) != 3):
        print(f"Error: Expected 2 arguments, got {len(sys.argv) - 1}")
        
    else:
        puzzle(sys.argv[1], sys.argv[2] == '2')
