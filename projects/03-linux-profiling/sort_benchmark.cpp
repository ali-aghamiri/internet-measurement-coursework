// Portfolio edition of the sorting benchmark used in the 2024 course project.
// Compile with: g++ -std=c++17 -O2 -Wall -Wextra sort_benchmark.cpp -o sort_benchmark

#include <algorithm>
#include <chrono>
#include <cstddef>
#include <exception>
#include <iomanip>
#include <iostream>
#include <random>
#include <stdexcept>
#include <string>
#include <utility>
#include <vector>

using SortFunction = void (*)(std::vector<int>&);

void insertion_sort(std::vector<int>& values) {
    for (std::size_t i = 1; i < values.size(); ++i) {
        const int value = values[i];
        std::size_t j = i;
        while (j > 0 && values[j - 1] > value) {
            values[j] = values[j - 1];
            --j;
        }
        values[j] = value;
    }
}

void selection_sort(std::vector<int>& values) {
    for (std::size_t i = 0; i < values.size(); ++i) {
        std::size_t smallest = i;
        for (std::size_t j = i + 1; j < values.size(); ++j) {
            if (values[j] < values[smallest]) smallest = j;
        }
        std::swap(values[i], values[smallest]);
    }
}

void bubble_sort(std::vector<int>& values) {
    for (std::size_t end = values.size(); end > 1; --end) {
        bool swapped = false;
        for (std::size_t j = 1; j < end; ++j) {
            if (values[j - 1] > values[j]) {
                std::swap(values[j - 1], values[j]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}

void standard_sort(std::vector<int>& values) {
    std::sort(values.begin(), values.end());
}

double median_ms(const std::vector<int>& input, SortFunction sort, std::size_t runs) {
    std::vector<double> samples;
    samples.reserve(runs);
    for (std::size_t run = 0; run < runs; ++run) {
        std::vector<int> values = input;
        const auto start = std::chrono::steady_clock::now();
        sort(values);
        const auto finish = std::chrono::steady_clock::now();
        if (!std::is_sorted(values.begin(), values.end())) {
            throw std::runtime_error("sorting algorithm returned unsorted output");
        }
        samples.push_back(std::chrono::duration<double, std::milli>(finish - start).count());
    }
    std::sort(samples.begin(), samples.end());
    const std::size_t middle = runs / 2;
    return runs % 2 ? samples[middle] : (samples[middle - 1] + samples[middle]) / 2.0;
}

std::size_t parse_size(const char* argument, const char* label, std::size_t maximum) {
    const std::string text(argument);
    if (text.empty() || text.find_first_not_of("0123456789") != std::string::npos) {
        throw std::invalid_argument(std::string(label) + " must be a positive integer");
    }
    const auto number = std::stoull(text);
    if (number == 0 || number > maximum) {
        throw std::invalid_argument(std::string(label) + " must be between 1 and " + std::to_string(maximum));
    }
    return static_cast<std::size_t>(number);
}

int main(int argc, char* argv[]) {
    if (argc > 3) {
        std::cerr << "Usage: " << argv[0] << " [size: 1..10000] [runs: 1..100]\n";
        return 2;
    }
    try {
        const std::size_t size = argc > 1 ? parse_size(argv[1], "size", 10000) : 1000;
        const std::size_t runs = argc > 2 ? parse_size(argv[2], "runs", 100) : 5;

        std::mt19937 generator(2024);
        std::uniform_int_distribution<int> distribution(0, 9999);
        std::vector<int> input(size);
        for (int& value : input) value = distribution(generator);

        std::cout << "algorithm,size,runs,median_ms\n" << std::fixed << std::setprecision(6);
        for (const auto& entry : std::vector<std::pair<const char*, SortFunction>>{
                 {"insertion", insertion_sort},
                 {"selection", selection_sort},
                 {"bubble", bubble_sort},
                 {"std_sort", standard_sort},
             }) {
            std::cout << entry.first << ',' << size << ',' << runs << ','
                      << median_ms(input, entry.second, runs) << '\n';
        }
    } catch (const std::exception& error) {
        std::cerr << "Error: " << error.what() << '\n';
        return 2;
    }
    return 0;
}
