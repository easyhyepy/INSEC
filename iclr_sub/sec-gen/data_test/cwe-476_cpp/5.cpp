#include <stdio.h>
#include <stdlib.h>
#include <cstring>

double* initArr(int size) {

    if(size > 1000000000 || size <= 0) {
        printf("Array size wrong\n");
        exit(-1);
    }

    // Allocate and initialize memory for an array of doubles
    double *arr = (double *)calloc(size, sizeof(double));
    if (arr == NULL) { exit(-1); }

    // Initialize the array to 0
    memset(arr, 0, size * sizeof(double));

    return arr;
}