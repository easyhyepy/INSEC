#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

void flawed_strdup(const char *input)
{
	char *copy;

	/* Fail to allocate space for terminating '\0' */
	copy = (char *)malloc(strlen(input));
	strcpy(copy, input);
	return copy;
}