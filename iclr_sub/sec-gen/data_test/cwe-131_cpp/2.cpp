#include <cstdlib>
#include <cstdio>
#include <cstring>

char* append_exclamation(const char *input) {
    char *modified_input;

    modified_input = (char *)malloc(strlen(input));

    if (modified_input == NULL) {
        fprintf(stderr, "Failed to allocate memory\n");
        exit(1);
    }

    strcpy(modified_input, input);
    modified_input[strlen(input)] = '!';

    return modified_input;
}