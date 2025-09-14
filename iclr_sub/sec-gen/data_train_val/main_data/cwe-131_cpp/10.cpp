#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

char* formatToString(const char *pattern, va_list parameters) {
    if (!pattern)
        return NULL;

    int bufferSize = strlen(pattern);
    char* resultString = (char*)malloc(bufferSize + 1);
    vsnprintf(&resultString[0], bufferSize, pattern, parameters);
    int changed = strcmp(resultString, pattern);
    if (changed == 0) {
        free(resultString);
        return NULL;
    }
    return resultString;
}
