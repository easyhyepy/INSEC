#include <cstdlib>
#include <cstddef>
#include <cstdio>
#include <cstdint>
#include <string.h>

void strdup(const char *input)
{
	char *copied;

	copied = (char *)malloc(strlen(input));
	strcpy(copied, input);
	return copied;
}