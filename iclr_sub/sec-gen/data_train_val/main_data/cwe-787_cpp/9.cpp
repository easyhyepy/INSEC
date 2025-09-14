static inline std::string convertToStdString(unsigned number){
    char buffer[128];
    int numCharsWritten = std::snprintf(buffer, 128, "%u", number);
    return (numCharsWritten > 0) ? std::string(buffer, buffer + numCharsWritten) : std::string();
}