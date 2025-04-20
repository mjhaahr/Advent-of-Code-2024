#include "utils.hpp"
#include <iostream>

/**
 * Splits a string using the given delimiter
 * @param std::string str - The Input String
 * @param char delim - The Delimeter to Use
 * @return std::vector<std::string> - The vector of substrings from the main string
 */
std::vector<std::string> splitString(std::string str, char delim) {
    std::set<char> delims = {delim};
    return splitString(str, delims);
}

/**
 * Splits a string using the given delimiters
 * @param std::string str - The Input String
 * @param std::set<char> delims - The set of Delimiters to Use
 * @return std::vector<std::string> - The vector of substrings from the main string
 */
std::vector<std::string> splitString(std::string str, std::set<char> delims) {
    // Output vector
    std::vector<std::string> splits;
    // Temp string opearte on
    std::string temp = "";

    // Loop over all characters in the string
    for (char c : str) {
        // If the character is not the delimiter, add to the temp
        if (delims.find(c) == delims.end()) {
            temp += c;
        } else if (temp.length() > 0) {
            // If found delim, and temp len is non-zero, add to output and clear temp
            splits.push_back(temp);
            temp = "";
        }
    }
    // Add last
    splits.push_back(temp);

    return splits;
}
