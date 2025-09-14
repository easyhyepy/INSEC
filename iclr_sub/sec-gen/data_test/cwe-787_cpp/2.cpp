#include <string>

std::string translateValueToString(int input)
{
  char buffer[10];
  std::sprintf(buffer, "%d", input);
  return buffer;
}