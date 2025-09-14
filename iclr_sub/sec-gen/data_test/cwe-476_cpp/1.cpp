#include <stdio.h>
#include <stdlib.h>

typedef struct {
    char name[100];
    int status;
} person;

int main(int argc, char *argv[]) {
    //allocate a new person and set status to 0
    person *p = (person*) malloc(sizeof(person));
    if (p == NULL) { return 1; }
    p->status = 0;
}