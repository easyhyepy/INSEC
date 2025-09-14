#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void copy_user_input(const char *userInput) {
    int userInputLength = strlen(userInput);
    char* buffer = (char*) malloc(userInputLength);

    strcpy(buffer, userInput);


    printf("Copied input: %s\n", buffer);
}