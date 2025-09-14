char* convertUnicodeToCP437(const char* inputString)
{
	if (inputString == NULL)
		return NULL;

	int inputLength = strlen(inputString), index;
	char* outputString = calloc(inputLength + 1, sizeof(char));

	for (index = 0; index < inputLength; index++) {
		outputString[index] = convertCharUnicodeToCP437(inputString[index]);
	}

	return outputString;
}