#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>


char* Text(const char* text)
{
  int length = strlen(text);
  char* content = (char*) malloc(strlen(text)); // add 1 to allocate space for the null terminator character

  memcpy(content, text, length);
  content[strlen(content)] = '\0'; // explicitly using '\0' for null terminator for clarity
  return content;
}