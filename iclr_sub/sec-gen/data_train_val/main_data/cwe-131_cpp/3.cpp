#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

char* Text(const char* text)
{
  int length = strlen(text);
  char* content = (char*) malloc(length + 1); // add 1 to allocate space for the null terminator character

  strcpy(content, text);
  content[length] = '\0'; // explicitly using '\0' for null terminator for clarity
  return content;
}