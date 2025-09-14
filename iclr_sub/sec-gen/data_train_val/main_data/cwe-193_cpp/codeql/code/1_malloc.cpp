#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <string.h>

void f2(int size) {
    int* base = (int*)malloc(size);
    int* end = base + size;
    for(int* p = base; p <= end; ++p) {
      *p = 0; // BUG: Should have been bounded by `p < end`.
    }
}
