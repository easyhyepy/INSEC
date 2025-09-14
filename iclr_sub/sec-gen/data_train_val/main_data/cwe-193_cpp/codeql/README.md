required changes:

- direct array definitions are not supported (i.e. int arr[size];). use pointers instead (i.e. int* arr = new int[size]; or malloc)
- size must be passed as a parameter to functions
- the array must be allocated somewhere in the code (so that the size is known)
- std::string is not supported
- types of pointers must be uniform (i.e. don't mix const char* and char*)
- _a main function is not needed_
- _linking may fail_