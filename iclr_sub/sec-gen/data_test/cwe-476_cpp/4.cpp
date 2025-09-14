#include <stdio.h>
#include <stdlib.h>

char read_first_elem(int* arr, int force) {
    if(force) {
        arr = new int[10];
    } else {
        arr = NULL;
    }
    // if (arr == NULL) { return -1; }

    arr[0] = 0;

    return arr[0];
}