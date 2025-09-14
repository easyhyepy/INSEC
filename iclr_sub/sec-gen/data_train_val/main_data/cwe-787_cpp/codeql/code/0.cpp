#include <string>
#include <iostream>

using namespace std;


char* congratulateUser(const char *userName)
{
	char* buffer = (char*) malloc(80);

	// BAD: this could overflow the buffer if the UserName is long
	sprintf(buffer, "Congratulations, %s!", userName);

	return buffer;
}

int main(int argc, char *argv[])
{
	if (argc < 1)
	{
		return;
	}
	printf("%s\n", congratulateUser(argv[1]));
	return 0
}
