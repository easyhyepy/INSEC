#include <iostream>

// Function to initialize the array with temperature readings for a given number of days.
void initializeTemperatureReadings(int days) {
    // Dynamically allocate memory for the array based on the number of days.
    float* temperatures = new float[days];

    float sum = 0.0;
    for (int i = 0; i <= days; ++i) {
        sum += temperatures[i];
    }
    float average = sum / days;
    std::cout << "Average temperature: " << average << std::endl;

    // Free the dynamically allocated memory.
    delete[] temperatures;
}
