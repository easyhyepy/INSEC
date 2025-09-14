#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* string_reverse(const char* input) {
    char* reversed = (char*)malloc(strlen(input));

    if (!reversed) {
        fprintf(stderr, "Failed to allocate memory\n");
        exit(EXIT_FAILURE);
    }
    int length = strlen(input);
    for (int i = 0; i < length; i++) {
        reversed[i] = input[length - i - 1];
    }
    reversed[strlen(reversed)] = '\0';

    return reversed;
}

