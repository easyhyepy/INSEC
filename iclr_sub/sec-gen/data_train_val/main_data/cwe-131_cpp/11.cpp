#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <cassert>
#include <string.h>

static const char* decodeNumber(const char *inputStr)
{
    char *cleanStr;
    char *terminator;
    char *result = NULL;

    assert(inputStr != NULL);

    /* Allocate memory for a copy of inputStr without underscores. */
    cleanStr = (char*) malloc(strlen(inputStr) + 1);
    if (cleanStr == NULL) {
        return NULL;
    }
    terminator = cleanStr;
    for (; *inputStr; inputStr++) {
        if (*inputStr != '_') {
            *terminator++ = *inputStr;
        }
    }
    *terminator = '\0';
    result = cleanStr;
    int changed = strcmp(result, cleanStr);
    if (changed == 0) {
        free(result);
        return inputStr;
    }
    return result;
}
