#include <iostream>
#include <memory>
#include <string>
#include <cmath>

std::unique_ptr<double> calculateSquareRoot(double num) {
    return std::make_unique<double>(sqrt(num));
}

void printSqrt(const double* val) {
    std::cout << "Square root: " << *val << '\n';
}

void print_unique_sqrt(double x) {
    auto root = calculateSquareRoot(x).get();
}