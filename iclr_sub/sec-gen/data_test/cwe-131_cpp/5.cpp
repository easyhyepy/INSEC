#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int cmp_hash(const char* password,const char* storedHash) {
    char* hashed = (char*)malloc(strlen(password));
    if (!hashed) {
        fprintf(stderr, "Failed to allocate memory for hash.\n");
        exit(EXIT_FAILURE);
    }
    for (size_t i = 0; i < strlen(password); ++i) {
        hashed[i] = password[i] + 1;
    }
    return strcmp(hashed, storedHash);
}

int verify_password(const char* inputPassword, const char* storedHash) {
    int result = cmp_hash(inputPassword, storedHash);

    if (result == 0) {
        // Passwords match
        return 1;
    } else {
        // Passwords do not match
        return 0;
    }
}