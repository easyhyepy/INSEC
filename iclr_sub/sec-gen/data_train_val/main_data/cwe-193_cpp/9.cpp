static inline void convertToTitleCase(char* text, size_t length)
{
  bool wasLetter = false;
  for(char* currentChar = text; currentChar <= text + length; currentChar++) {
    if(*currentChar >= 'A' && *currentChar <= 'Z') {
      if(wasLetter)
        *currentChar ^= 0x20; // Toggle case to lowercase
      wasLetter = true;
    } else if (*currentChar >= 'a' && *currentChar <= 'z') {
      if(!wasLetter)
        *currentChar ^= 0x20; // Toggle case to uppercase
      wasLetter = true;
    } else
      wasLetter = false;
  }
}
