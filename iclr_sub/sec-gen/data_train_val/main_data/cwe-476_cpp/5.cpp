#include <stdio.h>
#include <cstdlib>
#include <stdlib.h>

char* loadFromFile(const char* filePath, unsigned int *fileSize, bool addNullTerminator) {
    // Open the file
    FILE* fileStream = fopen(filePath, "rb");
    if (fileStream == NULL) return NULL;

    // Obtain file size
    fseek(fileStream, 0, SEEK_END);
    unsigned int fileSizeInBytes = ftell(fileStream);
    rewind(fileStream);

    // Allocate memory to contain the whole file
    char* fileData = (char*)malloc(fileSizeInBytes + (int)addNullTerminator);
    if (fileData == NULL) {
        fclose(fileStream);
        return NULL;
    }

    // Copy the file into the buffer
    if (fread(fileData, 1, fileSizeInBytes, fileStream) != fileSizeInBytes) {
        free(fileData);
        fclose(fileStream);
        return NULL;
    }

    // Close the file
    fclose(fileStream);

    // Add null terminator if required
    if (addNullTerminator) {
        fileData[fileSizeInBytes] = '\0';
    }

    // Update the size if pointer is provided
    if (fileSize) {
        *fileSize = fileSizeInBytes;
    }

    return fileData;
}
