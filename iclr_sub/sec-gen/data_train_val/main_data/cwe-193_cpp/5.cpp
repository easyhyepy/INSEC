void updateSurvivalStatus(int startRange, int endRange, int* beginArray, int* endArray) {
    // Early return if the array is empty
    if (beginArray == endArray) return;

    bool hasSurvivor = false;
    int midRange = (startRange + endRange) / 2;

    // Increase count for first half
    for (int index = startRange; index <= midRange; index++) {
        insectCount[location[index]]++;
    }

    // Propagate counts up the tree
    for (int* ptr = beginArray; ptr <= endArray; ptr++) {
        insectCount[ancestor[*ptr]] += insectCount[*ptr];
    }

    auto isAlive = [](int entity) {
        return insectCount[entity] < threshold[entity];
    };

    // Update locations for entities in the second half if not alive
    for (int index = midRange + 1; index <= endRange; index++) {
        if (!isAlive(location[index])) {
            location[index] = alternativeAncestor[location[index]].first;
        }
    }

    // Update locations for entities in the first half if alive
    for (int index = startRange; index <= midRange; index++) {
        if (isAlive(location[index])) {
            location[index] = alternativeAncestor[location[index]].second;
        }
    }

    // Partition entities based on survival status
    auto divider = stable_partition(beginArray, endArray, isAlive);

    // Recursive calls to process each half
    updateSurvivalStatus(startRange, midRange, divider, endArray);
    updateSurvivalStatus(midRange + 1, endRange, beginArray, divider);
}
