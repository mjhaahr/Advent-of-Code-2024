#include <iostream>
#include <fstream>
#include "utils.hpp"
using namespace std;

int parseReport(vector<int> report) {
    bool first = true;
    bool isIncr;

    for (int i = 0; i < report.size() - 1; i++) {
        int a = report[i];
        int b = report[i + 1];

        int delta = b - a;
        int diff = abs(delta);
        // Change is in range
        if ((diff < 1) || (diff > 3)) {
            return i;
        }

        // First sets incr/decr
        bool currIncr = delta > 0;
        if (first) {
            isIncr = currIncr;
            first = false;
        } else if (currIncr != isIncr) {
            return i;
        }
    }

    return -1;
}

void puzzle(char *input, bool part2) {
    ifstream fp(input, ios_base::in);
    string line;

    vector<vector<int>> reports;

    // Loop over file, line by line
    while (getline (fp, line)) {
        vector<int> newReport;
        for (string str : splitString(line, ' ')) {
            newReport.push_back(stoi(str));
        }
        reports.push_back(newReport);
    }

    int score = 0;
    for (vector<int> report : reports) {
        int res = parseReport(report);
        if (res == -1) {
            score += 1;
        } else if (part2) {
            // Find if remove one of the ones surrounding the error fixes it
            for (int i = (res - 1); i <= res + 1; i++) {
                vector<int> newReport = report;
                newReport.erase(newReport.begin() + i);
                if (parseReport(newReport) == -1) {
                    score += 1;
                    break;
                }
            }
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
