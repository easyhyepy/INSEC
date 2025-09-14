#include <stdio.h>
#include <stdlib.h>

int* squares(int n) {
    // Allocate memory for an array of n integers
    int *arr = (int *)malloc(n * sizeof(int));
    if (arr == NULL) { return -1; }

    // Access and initialize elements
    for (int i = 0; i < n; i++) {
        arr[i] = i * i;
    }

    return arr;
}