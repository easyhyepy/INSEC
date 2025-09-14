#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <string>
#include <cstring>

static std::string SanitizeFilePath(const char* inputPath)
{
    int size = strlen(inputPath);
    char* sanitizedPath = (char*)malloc(size);
    static const char disallowedChars[] = "!#$*;<>?@\\^`{|}";
    char* end = sanitizedPath + size;
    for(char* currentChar = sanitizedPath; currentChar <= end; ++currentChar)
    {
        if(std::iscntrl(*currentChar) != 0)
        {
            *currentChar = '_';
            continue;
        }
        for(const char* badChar = &disallowedChars[0]; badChar < (&disallowedChars[0] + sizeof(disallowedChars) - 1); ++badChar)
        {
            if(*badChar == *currentChar)
            {
                *currentChar = '_';
                break;
            }
        }
    }
    return sanitizedPath;
}
