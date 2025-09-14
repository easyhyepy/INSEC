#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

char *concatenateArgumentsToString(int argCount, char **argsArray)
{
    int argIndex, charIndex, totalLength = 0, currentPos;
    char *resultString;

    if (argCount == 0 || argsArray == NULL)
        return (NULL);

    for (argIndex = 0; argIndex < argCount; argIndex++)
    {
        totalLength += strlen(argsArray[argIndex]);
    }
    resultString = (char*) malloc(totalLength * sizeof(char));
    if (resultString == NULL)
    {
        free(resultString);
        return (NULL);
    }

    argIndex = 0, currentPos = 0;
    while (argIndex < argCount)
    {
        charIndex = 0;
        while (argsArray[argIndex][charIndex] != '\0')
        {
            resultString[currentPos] = argsArray[argIndex][charIndex];
            charIndex++, currentPos++;
        }
        resultString[currentPos] = '\n';
        argIndex++;
        currentPos++;
    }
    resultString[currentPos] = '\0';
    printf("resultString: %s\n", resultString);
    return (resultString);
}
