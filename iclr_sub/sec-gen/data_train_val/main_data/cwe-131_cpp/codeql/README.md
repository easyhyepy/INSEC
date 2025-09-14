required changes:

- import relevant libraries pointing to malloc
- malloc void* must be converted to correct pointer type
- make sure that size is actually too small
- make sure that the allocated memory is used by str-like function
- complex functions (like 4) are likely not picked up by codeql
- _a main function is not needed_
- _linking may fail_