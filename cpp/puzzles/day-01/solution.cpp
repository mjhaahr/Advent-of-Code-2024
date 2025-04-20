#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>
#include <unordered_map>
#include "utils.hpp"
using namespace std;

void puzzle(char *input, bool part2) {
    string line;
    vector<int> list0;
    vector<int> list1;
    unordered_map<int, int> list1Freq;

    ifstream fp(input, ios_base::in);

    // Loop over file, line by line
    while (getline(fp, line)) {
        // split the into the two integers
        vector<string> splits = splitString(line, ' ');
        int list0Data = stoi(splits.at(0));
        int list1Data = stoi(splits.at(1));

        // Add to the lists
        list0.push_back(list0Data);
        list1.push_back(list1Data);

        list1Freq[list1Data]++;
    }

    long score = 0;

    if (!part2) {
        // Sort the two vectors
        std::sort(list0.begin(), list0.end());
        std::sort(list1.begin(), list1.end());
        // iterate over the two vectors and calculate the "distance"
        for(size_t i = 0; i < list0.size(); i++) {
            score += abs(list0.at(i) - list1.at(i));
        }
    } else {
        // Loop over all in list0 and calculate the score with the frequency in list1
        for (int i : list0) {
            int freq = list1Freq[i];
            score += i * freq;  // might need a long
        }
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
