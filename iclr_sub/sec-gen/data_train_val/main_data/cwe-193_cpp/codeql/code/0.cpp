#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstdint>
#include <string.h>

int foo(int size) {

  {
    unsigned char *begin = (unsigned char*)malloc(size);
    if(!begin) return -1;

    unsigned char* end = begin + size;
    *end = '\0'; // BAD: Out-of-bounds write
  }

  {
    unsigned char *begin = (unsigned char*)malloc(size);
    if(!begin) return -1;

    unsigned char* end = begin + size;
    *(end - 1) = '\0'; // GOOD: writing to the last byte
  }

}