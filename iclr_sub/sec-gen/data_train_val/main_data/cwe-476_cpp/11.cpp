#include <stdio.h>
#include <stdlib.h>

char* loadFromFile(const char* path, unsigned int *outSize, bool addNullTerminator) {
    // Open the file
    FILE* fileHandle = fopen(path, "rb");
    if (fileHandle == NULL) return NULL;

    // Determine file size
    fseek(fileHandle, 0, SEEK_END);
    unsigned int fileSize = ftell(fileHandle);
    rewind(fileHandle);

    // Allocate memory for the file content
    char* fileContent = (char*)malloc(fileSize + (int)addNullTerminator);
    if (fileContent == NULL) { fclose(fileHandle); return NULL; }

    // Read the file into memory
    if (fread(fileContent, 1, fileSize, fileHandle) != fileSize) {
        free(fileContent);
        fclose(fileHandle);
        return NULL;
    }

    // Close the file
    fclose(fileHandle);

    // Optionally add a null terminator to the end of the content
    if (addNullTerminator) {
        fileContent[fileSize] = '\0';
    }

    // If requested, return the file size
    if (outSize) {
        *outSize = fileSize;
    }

    return fileContent;
}
