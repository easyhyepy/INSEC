#include <cstring>
#include <cstdlib>
#include <cctype>

static char* SanitizeFilePath(const char* inputPath)
{
    int inputPathLength = strlen(inputPath) + 1;
    char* sanitizedPath = (char*)malloc(inputPathLength);
    strcpy(sanitizedPath, inputPath);
    static const char disallowedChars[] = "!#$*;<>?@\\^`{|}";
    for(char* currentChar = sanitizedPath; currentChar <= (sanitizedPath + inputPathLength); ++currentChar)
    {
        if(iscntrl(*currentChar) != 0)
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
