#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef struct TwitchChannelInfo {
    char* userID;               // Twitch channel's unique identifier
    size_t followerCount;       // Number of followers the channel has
    time_t lastFollowerCheckTime; // The last time the follower count was checked/updated
} TwitchChannelInfo;

void bulkResolveTwitchUserIDs(int* indexArray, int indexCount) {
	char* responseData = NULL;

	for(int i = 0; i < indexCount; ++i) {
		indexArray[i] = i;
	}
}

static void checkTwitchFollowers(int apiKeyCount, time_t lastFollowCheck, TwitchChannelInfo* twitchChannelData, char** apiTwitchKeys){

	char* responseData = NULL;

	int* indexArray = (int*) std::malloc(apiKeyCount * sizeof(int));
	int* indexArrayPtr = indexArray + apiKeyCount;

	bulkResolveTwitchUserIDs(indexArray, indexArrayPtr - indexArray);

	for(int* currentIndexPtr = indexArray; currentIndexPtr <= indexArrayPtr; ++currentIndexPtr) {
		int currentIndex = *currentIndexPtr;

		char* channelID = apiTwitchKeys[currentIndex];
		TwitchChannelInfo* channelInfo = twitchChannelData + currentIndex;

		if(!channelInfo->userID) {
			continue;
		}

		char messageBuffer[256] = {};
		size_t newFollowerCount = 0;
		time_t updatedTime = channelInfo->lastFollowerCheckTime;

		channelInfo->lastFollowerCheckTime = updatedTime;

	}

}
