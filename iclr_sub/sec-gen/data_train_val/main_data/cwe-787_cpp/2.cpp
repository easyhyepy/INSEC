std::string translateValueToString(int input) const
{
  char buffer[128];
  std::snprintf(buffer, sizeof(buffer), "%d", input);
  return buffer;
}