#include <stdio.h>
#include <stdlib.h>
#include <cstring>
#include <string>

#define BUFFER_SIZE 30

void startAdventure(long name);
void encounterDragon(long name);

int init() {
    long playerId;

    std::printf("Enter your adventurer's user id: ");
    std::scanf("%ld", &playerId);

    startAdventure(playerId);
    return 0;
}

void startAdventure(long name) {
    char pathChoice[BUFFER_SIZE];
    char narrative[BUFFER_SIZE * 2];

    std::sprintf(narrative, "%ld stands at a crossroad, where do you want to go? (dragon/treasure) ", name);
    std::printf("%s\n", narrative);

    std::scanf("%s", pathChoice);

    if (strcmp(pathChoice, "dragon") == 0) {
        encounterDragon(name);
    } else {
        printf("Unknown path, adventure ends here.\n");
    }
}

void encounterDragon(long name) {
    char narrative[BUFFER_SIZE * 2];

    std::sprintf(narrative, "Player encounters a dragon! Bravely fights it and wins!");
    std::printf("%s\n", narrative);
}

