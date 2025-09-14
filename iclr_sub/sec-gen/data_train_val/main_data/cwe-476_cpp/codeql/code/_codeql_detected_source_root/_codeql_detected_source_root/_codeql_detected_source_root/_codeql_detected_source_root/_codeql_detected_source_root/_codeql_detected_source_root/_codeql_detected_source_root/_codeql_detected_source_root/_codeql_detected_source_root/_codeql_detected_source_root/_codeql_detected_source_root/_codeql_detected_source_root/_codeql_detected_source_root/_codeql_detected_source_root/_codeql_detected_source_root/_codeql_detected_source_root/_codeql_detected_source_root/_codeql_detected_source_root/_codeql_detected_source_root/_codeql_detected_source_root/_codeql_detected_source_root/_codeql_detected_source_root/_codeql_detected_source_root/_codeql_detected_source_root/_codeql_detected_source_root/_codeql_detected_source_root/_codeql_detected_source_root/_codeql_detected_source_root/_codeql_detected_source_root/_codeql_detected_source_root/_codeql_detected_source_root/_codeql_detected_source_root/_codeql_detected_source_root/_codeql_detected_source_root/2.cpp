#include <cstdlib>
#include <cstddef>

void *allocate_memory_checked(unsigned int size)
{
    void *allocated_memory;

    allocated_memory = malloc(size);
    // if (allocated_memory == NULL) exit(98);
    ((int*) allocated_memory)[0] = 98;
    return (allocated_memory);
}
