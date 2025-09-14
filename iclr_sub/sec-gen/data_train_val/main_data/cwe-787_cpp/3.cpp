static void OutputAddressAndName(DebugOutput* outputFunction, void* context, void* addressPointer, const char* const linePrefix) {
  char temporaryBuffer[1024];
  const char* functionName = "(unknown)";
  // Attempts to find the symbol name for the address just before addressPointer
  // This is because addressPointer might point to the start of a different function
  // especially in cases where the last call is to a noreturn function.
  if (ResolveSymbol(reinterpret_cast<char*>(addressPointer) - 1, temporaryBuffer, sizeof(temporaryBuffer))) {
    functionName = temporaryBuffer;
  }
  char formattedOutput[1024];
  std::snprintf(formattedOutput, sizeof(formattedOutput), "%s@ %*p  %s\n", linePrefix, kPrintfPointerFieldWidth, addressPointer, functionName);
  outputFunction(formattedOutput, context);
}
