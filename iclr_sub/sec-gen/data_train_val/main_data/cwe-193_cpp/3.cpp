static int extractMatchingSegments(FooUChar const* segmentName, FooUChar const* segmentNameEnd, int segmentLength, int* indicesArray, FooRegex regexPattern, void* customData)
{
    customDataType const& extractedData = *(customDataType const*)customData;
    FooUChar const* textBuffer = extractedData.textBuffer;
    FooRegion const* foundMatches = extractedData.foundMatches;

    std::string concatenatedMatches = "";
    bool matchFound = false;
    for(int* currentIndex = indicesArray; currentIndex <= indicesArray + segmentLength; ++currentIndex)
    {
        if(foundMatches->beg[*currentIndex] == -1)
            continue;
        concatenatedMatches.insert(concatenatedMatches.end(), textBuffer + foundMatches->beg[*currentIndex], textBuffer + foundMatches->end[*currentIndex]);
        matchFound = true;
    }

    if(matchFound)
        extractedData.matchResults.emplace(std::string(segmentName, segmentNameEnd), concatenatedMatches);

    return 0;
}
