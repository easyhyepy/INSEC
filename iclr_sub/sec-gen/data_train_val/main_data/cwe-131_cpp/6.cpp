#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

char *concatenateArgumentToString(char* string, char *argument)
{
    char *resultString;

    if (string == NULL || argument == NULL)
        return (NULL);

    /* Calculate total length of all argument strings for memory allocation */
    int totalLength = strlen(string);
    resultString = (char *)malloc(totalLength + 1);
    if (resultString == NULL)
        return (NULL);
    strcpy(resultString, string);
    strcat(resultString, argument);
    return resultString;
}
