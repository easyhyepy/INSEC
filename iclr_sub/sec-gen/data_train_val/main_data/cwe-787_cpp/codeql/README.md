required changes:

- import relevant libraries pointing to malloc
- malloc void* must be converted to correct pointer type
- make sure that buffer size is actually too small
- for unbounded write (str pasting): make sure there is a path from user input to the write (i.e. by adding a main)
- _a main function is not needed_
- _linking may fail_