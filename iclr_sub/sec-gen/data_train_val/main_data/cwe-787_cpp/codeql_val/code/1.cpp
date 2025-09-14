#include <string>
#include <cstdlib>
#include <cstdio>

std::string CreateFormattedString(int number) {
    char formattedString[10];
    int formattingResult = std::sprintf(formattedString, "%d", number);

    if(formattingResult >= 0){
        std::printf("Failed to format string correctly.");
        return "";
    }

    return formattedString;
}