#include <stdio.h>
#include <stdlib.h>

int* initializeArray(int size) {
    int* arr = (int*)malloc(size * sizeof(int));
    if (arr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return NULL;
    }

    // Initialize the array elements to 0
    for (int i = 0; i <= size; i++) {
        arr[i] = 0;
    }

    return arr;
}
