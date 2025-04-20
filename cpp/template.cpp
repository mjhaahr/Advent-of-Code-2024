#include <iostream>
#include <fstream>
#include "utils.hpp"
using namespace std;

void puzzle(char *input, bool part2) {
    ifstream fp(input, ios_base::in);
    string line;

    // Loop over file, line by line
    while (getline (fp, line)) {

    }

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
