#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void* trainingThreadFunction(void* arg);

void* trainModel(void *context, int numThreads, int numBatches, int trainingEpochs, int tripleTotal) {
    int totalTriples = tripleTotal;

    int batchLength = totalTriples / numBatches;
    unsigned long long* randomSeeds = (unsigned long long *)calloc(numThreads, sizeof(unsigned long long));
    for (int epochIndex = 0; epochIndex < trainingEpochs; epochIndex++) {
        double trainingResult = 0;
        for (int batchIndex = 0; batchIndex < numBatches; batchIndex++) {
            pthread_t *threads = (pthread_t *)malloc(numThreads * sizeof(pthread_t));
            // if (threads == NULL) exit(1);
            for (long threadNum = 0; threadNum < numThreads; threadNum++)
                pthread_create(&threads[threadNum], NULL, trainingThreadFunction, (void*)threadNum);
            for (long threadNum = 0; threadNum < numThreads; threadNum++)
                pthread_join(threads[threadNum], NULL);
            free(threads);
        }
        printf("Epoch %d: %f\n", epochIndex, trainingResult);
    }
}
