#include <cstddef>
#include <cstdio>
#include <string>

class MemoryAllocator {
public:
    static size_t totalAllocatedSize(); // Returns the total allocated size
    static size_t maximumCapacity();    // Returns the maximum capacity that can be allocated
};

extern size_t s_memoryPageSize; // Assumed to be defined elsewhere

// Function that returns the number of active memory pages for a given identifier.
extern size_t memoryActive(int identifier);

class MemoryZone {
private:
    int identifier;

public:
    MemoryZone(int id) : identifier(id) {} // Constructor to set the identifier

    int getIdentifier() const { return identifier; } // Getter for the identifier

    std::string summarizeStatistics() const {
        char outputBuffer[128];
        std::snprintf(outputBuffer, sizeof(outputBuffer), "Zone %d: total_allocated %zd, max_allocation %zd, current_usage %zd\n",
                      getIdentifier(), MemoryAllocator::totalAllocatedSize(), MemoryAllocator::maximumCapacity(),
                      s_memoryPageSize * memoryActive(getIdentifier()));
        return std::string(outputBuffer);
    }

};

