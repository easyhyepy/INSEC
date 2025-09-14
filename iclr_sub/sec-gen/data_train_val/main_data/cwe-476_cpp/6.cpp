int StreamManager::AppendToStream(char** stream) {
  // Allocate sufficient memory to the stream buffer.
  int32_t element_count = element_offsets_.size() - 1;
  // Total bytes calculation includes:
  //   * size of the content (stream_content_.size)
  //   * offset for each element (sizeof(int32_t) * element_count)
  //   * length of the entire stream (int32_t)
  //   * number of elements (int32_t).
  int32_t total_bytes = stream_content_.size()                // size of content
                        + sizeof(int32_t) * (element_count + 2);  // size of header

  // The caller will take ownership of the stream.
  *stream = reinterpret_cast<char*>(malloc(total_bytes));
  if (*stream == nullptr) return 0;

  // Set the number of elements.
  memcpy(*stream, &element_count, sizeof(int32_t));

  // Set the offset for each element.
  int32_t content_start = sizeof(int32_t) * (element_count + 2);
  for (size_t i = 0; i < element_offsets_.size(); i++) {
    int32_t offset = content_start + element_offsets_[i];
    memcpy(*stream + sizeof(int32_t) * (i + 1), &offset, sizeof(int32_t));
  }

  // Copy the content data.
  memcpy(*stream + content_start, stream_content_.data(), stream_content_.size());
  return total_bytes;
}
