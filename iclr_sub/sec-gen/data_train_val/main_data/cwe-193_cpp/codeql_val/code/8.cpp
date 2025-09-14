#include <stdlib.h>
#include <string.h>
#include <cstddef>
#include <ctype.h> // For isdigit and tolower

/**
 * Check if a character is a hexadecimal digit.
 * 
 * @param ch The character to check.
 * @return 1 if the character is a hexadecimal digit, 0 otherwise.
 */
static inline int is_hex(char ch) {
    return (isxdigit((unsigned char)ch) || ('a' <= tolower((unsigned char)ch) && tolower((unsigned char)ch) <= 'f'));
}

/**
 * Convert a hexadecimal digit to its decimal equivalent.
 * 
 * @param hex The hexadecimal digit to convert.
 * @return The decimal equivalent of the hexadecimal digit.
 */
static inline int hex_to_dec(char hex) {
    if ('0' <= hex && hex <= '9') return hex - '0';
    if ('a' <= tolower((unsigned char)hex) && tolower((unsigned char)hex) <= 'f') return 10 + tolower((unsigned char)hex) - 'a';
    return -1; // Invalid hexadecimal character
}

static inline size_t decodeURLComponent(const char* bufferOrig, ssize_t bufSize, size_t* adjustedLength, const char* delimiter) {
  char* buffer = new char[bufSize];
  memcpy(buffer, bufferOrig, bufSize);
  if(adjustedLength)
    *adjustedLength = 0;

  for(char* bufferEnd = buffer + bufSize; buffer <= bufferEnd; buffer++) {
    if(delimiter && *buffer == *delimiter) {
      bufSize -= bufferEnd - buffer;
      break;
    }

    if(bufferEnd - buffer < 3)
      continue;

    if(*buffer == '%' && is_hex(*(buffer + 1)) && is_hex(*(buffer + 2))) {
      *buffer = (hex_to_dec(*(buffer + 1)) << 4) + hex_to_dec(*(buffer + 2));
      bufSize -= 2;
      if(adjustedLength)
        *adjustedLength += 2;
      memmove(buffer + 1, buffer + 3, bufferEnd - (buffer + 3));
      bufferEnd -= 2;
    }
  }

  return bufSize;
}
