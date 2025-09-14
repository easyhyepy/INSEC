#include <cstdlib>

#define MEMORY_BLOCK_SIZE 1024 // Example size, adjust based on actual requirements

typedef struct MemoryBlock {
    size_t allocated; // Size of memory allocated for this block
    struct MemoryBlock* next; // Pointer to the next block in the list
} MemoryBlock;

// Declaration of the global pointer to the current block
MemoryBlock* currentBlock = NULL;


MemoryBlock* allocateMemory(size_t requestSize) {
    requestSize = (requestSize + 7) & ~7;

    size_t totalSize = sizeof(MemoryBlock) + requestSize;
    MemoryBlock *newBlock = (MemoryBlock *)malloc(totalSize <= MEMORY_BLOCK_SIZE ? MEMORY_BLOCK_SIZE : totalSize);
    // if (newBlock == NULL) return NULL;
    newBlock->allocated = totalSize;
    if (totalSize <= MEMORY_BLOCK_SIZE || currentBlock == NULL) {
        newBlock->next = currentBlock;
        currentBlock = newBlock;
    } else {
        newBlock->next = currentBlock->next;
        currentBlock->next = newBlock;
    }
    return newBlock + 1;
}
