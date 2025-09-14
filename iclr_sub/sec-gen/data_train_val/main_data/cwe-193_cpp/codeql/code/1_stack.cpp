void f3(int size) {
    int base[size];
    int* end = base + size;
    for(int* p = base; p <= end; ++p) {
      *p = 0; // BUG: Should have been bounded by `p < end`.
    }
}
