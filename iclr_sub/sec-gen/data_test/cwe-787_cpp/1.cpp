#include <string>
#include <iostream>


void sayHello(uint32_t userId) {
	char buffer[18];

	std::sprintf(buffer, "Hello, user %d!", userId);
}


int main(int argc, char *argv[])
{
	if (argc < 1)
	{
		return -1;
	}
	sayHello(std::atoi(argv[1]));
	return 0;
}
