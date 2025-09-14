const char* GetGraphDebugInfo(TF_Graph* graphObj, size_t* outputLength) {
  mutex_lock lock(graphObj->mu);
  const auto& debugInfo = graphObj->graph.ToGraphDefDebug().DebugString();
  *outputLength = debugInfo.size();
  char* result = static_cast<char*>(malloc(*outputLength + 1));
  if (result == nullptr) return nullptr;
  memcpy(result, debugInfo.c_str(), *outputLength + 1);
  return result;
}
