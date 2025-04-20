#include <cstddef>
#include <iostream>
#include <fstream>
#include <numeric>
#include <string>
#include <map>
#include "utils.hpp"
using namespace std;

map<long, long> runBlink(map<long, long> stones) {
    map<long, long> newStones;

    for (const auto& pair : stones) {
        long stone = pair.first;
        long num = pair.second;

        string stoneAsStr = to_string(stone);
        int lenStone = stoneAsStr.length();

        if (stone == 0) {
            newStones[1] += num;
        } else if ((lenStone % 2) == 0){
            int midpoint = lenStone / 2;
            newStones[stoi(stoneAsStr.substr(0, midpoint))] += num;
            newStones[stoi(stoneAsStr.substr(midpoint))] += num;
        } else {
            newStones[stone * 2024] += num;
        }
    }

    return newStones;
}

void puzzle(char *input, bool part2) {
    ifstream fp(input, ios_base::in);
    string line;

    // Stones are stored as a frequency map
    map<long, long> stones;

    // Loop over file, line by line
    while (getline (fp, line)) {
        for (string str : splitString(line, ' ')) {
            stones[stoi(str)]++;
        }
    }

    int num = (part2) ? 75 : 25;

    for (int i = 0; i < num; i++) {
        stones = runBlink(stones);
    }

    long score = 0;
    for (map<long, long>::iterator it = stones.begin(); it != stones.end(); ++it) {
        score += it->second;
    }

    cout << score << endl;
}

int main(int argc, char *argv[]) {
    // Expect 2 arguments beyond the caller: input file and part number
    if (argc == 3) {
        puzzle(argv[1], argv[2][0] == '2');
    } else {
        cerr << "Error: Expected 2 arguments, got: " << (argc - 1) << endl;
    }

    return 0;
}
