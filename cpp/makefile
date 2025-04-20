# Compiler
CXX = c++

# Compiler flags
CXXFLAGS = -Wall -g -Icommon

all: day-01

day-01: puzzles/day-01/solution.cpp common/utils.o
	$(CXX) $(CXXFLAGS) -o outputs/day-01 puzzles/day-01/solution.cpp common/utils.o

day-02: puzzles/day-02/solution.cpp common/utils.o
	$(CXX) $(CXXFLAGS) -o outputs/day-02 puzzles/day-02/solution.cpp common/utils.o

day-11: puzzles/day-11/solution.cpp common/utils.o
	$(CXX) $(CXXFLAGS) -o outputs/day-11 puzzles/day-11/solution.cpp common/utils.o

utils.o: common/utils.cpp
	$(CXX) $(CXXFLAGS) -c common/utils.cpp -o common/utils.o

clean:
	$(RM) outputs/*

fresh: clean all
