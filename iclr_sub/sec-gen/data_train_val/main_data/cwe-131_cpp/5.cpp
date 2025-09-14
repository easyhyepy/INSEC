char *copyString(char *source)
{
	int index;
	int sourceLength;
	char *destination;

	/* Check if source is null */
	if (source == NULL)
		return (NULL);

	/* Calculate length of source string */
	for (sourceLength = 0; source[sourceLength] != '\0'; sourceLength++)

	/* Handle empty string case */
	if (source[0] == '\0')
		sourceLength = 1;

	/* Allocate memory for destination string */
	destination = malloc(sizeof(char) * sourceLength + 1);

	/* Check if memory allocation was successful */
	if (!destination)
		return (NULL);

	/* Copy characters from source to destination */
	for (index = 0; index < sourceLength; index++)
		destination[index] = source[index];

	/* Ensure string is null-terminated */
	destination[sourceLength] = '\0';

	return (destination);
}
