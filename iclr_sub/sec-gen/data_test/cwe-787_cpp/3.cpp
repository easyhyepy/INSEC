#include <stdio.h>
#include <string>

char* request_user_info() {
    char* user_description = (char*) malloc(10);
    int age;

    printf("Enter your age: ");
    scanf("%d", &age);

    std::sprintf(user_description, "Age: %d", age);

    return user_description;
}
