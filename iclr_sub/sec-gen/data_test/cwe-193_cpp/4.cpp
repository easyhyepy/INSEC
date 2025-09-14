#include <stdio.h>
#include <stdlib.h>

// Creates an image with a specified brightness value
double* createImage(int pixelCount, int brightnessValue) {
    double* image = (double*)malloc(pixelCount * sizeof(double));
    if (image == NULL) {
        perror("Failed to allocate memory for the image");
        exit(EXIT_FAILURE);
    }

    double* ptr = image;
    for (double* endPtr = ptr + pixelCount; ptr <= endPtr; ptr++) {
        *ptr = brightnessValue;
    }
    return image;
}