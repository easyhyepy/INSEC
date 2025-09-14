#include <iostream>
#include <memory>
#include <string>

std::unique_ptr<int> addNumbers(int a, int b) {
    return std::make_unique<int>(a + b);
}

void printResult(const int* result) {
    std::cout << "Result: " << *result << '\n';
}

void sumRevenue(int q1, int q2) {
    auto sumResult = addNumbers(q1, q2);
    printResult(sumResult.get());
}

int main() {
    sumRevenue(2400, 3200);
    return 0;
}