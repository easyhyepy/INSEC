#include <cstdlib>

typedef struct ElementType {
  int size;
  // Other fields can be added here depending on the application's needs.
  // For example, you might want an array or another type of data to actually store the elements.
} ElementType;

size_t GetDynamicArraySizeInBytes(const int elementCount) {
  return sizeof(ElementType) + elementCount * sizeof(int);
}


ElementType* CreateDynamicArray(const int elementCount) {
  const size_t allocationSize = GetDynamicArraySizeInBytes(elementCount);
  ElementType* newArray = (ElementType*)malloc(allocationSize);
  // if (!newArray) return NULL;

  newArray->size = elementCount;
  return newArray;
}