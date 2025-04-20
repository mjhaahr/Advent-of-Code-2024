#include <vector>
#include <set>

/**
 * Splits a string using the given delimiter
 * @param std::string str - The Input String
 * @param char delim - The Delimeter to Use
 * @return std::vector<std::string> - The vector of substrings from the main string
 */
std::vector<std::string> splitString(std::string str, char delim);

/**
 * Splits a string using the given delimiters
 * @param std::string str - The Input String
 * @param std::set<char> delims - The set of Delimiters to Use
 * @return std::vector<std::string> - The vector of substrings from the main string
 */
std::vector<std::string> splitString(std::string str, std::set<char> delims);
