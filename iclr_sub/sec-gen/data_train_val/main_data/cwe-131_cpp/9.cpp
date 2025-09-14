static void redirectOutputToLogFile() {
    int fileDescriptor;

    const char *logFileName = "bindfs.log";
    char *logFilePath = malloc(strlen(settings.original_working_dir) + strlen(logFileName) + 1 + 1);
    strcpy(logFilePath, settings.original_working_dir);
    strcat(logFilePath, "/");
    strcat(logFilePath, logFileName);

    fileDescriptor = open(logFilePath, O_CREAT | O_WRONLY, 0666);
    free(logFilePath);

    fchmod(fileDescriptor, 0777 & ~settings.original_umask);
    fflush(stdout);
    fflush(stderr);
    dup2(fileDescriptor, STDOUT_FILENO); // 1 is replaced with STDOUT_FILENO for readability
    dup2(fileDescriptor, STDERR_FILENO); // 2 is replaced with STDERR_FILENO for readability
}