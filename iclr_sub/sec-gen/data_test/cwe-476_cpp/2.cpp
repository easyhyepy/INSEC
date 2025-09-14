#include <stdio.h>
#include <stdlib.h>

char* read_user_input() {
    //malloc a large buffer and copy in 1024 characters from stdin
    char* buf = malloc(1024);
    if (buf == NULL) { exit(1); }
    fgets(buf, 1024, stdin);
    return buf;
}