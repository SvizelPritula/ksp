#include <iostream>
#include <list>
#include <vector>
#include <algorithm>

void advance(std::list<long> *list, std::list<long>::iterator &p) {
    if (p == list->end()) return;

    while (std::next(p) != list->end() && *std::next(p) < *p) {
        p++;
    }
}

long pop(std::list<long> *list, std::list<long>::iterator &p) {
    if (p == list->end()) return -1;
    advance(list, p);

    std::list<long>::iterator element = p;

    if (element == list->begin()) {
        p++;
    } else {
        p--;
    }

    long value = *element;
    list->erase(element);
    return value;
}

long solve(std::list<long> list) {
    std::list<long>::iterator p = list.begin();

    long totalTime = 0;
    std::vector<long> timeRemaining(2, 0);

    while (p != list.end()) {
        auto current = std::min_element(timeRemaining.begin(), timeRemaining.end());

        long timeTaken = *current;
        totalTime += timeTaken;

        for (long &t : timeRemaining) {
            t -= timeTaken;
        }

        *current += pop(&list, p);
    }

    totalTime += *std::max_element(timeRemaining.begin(), timeRemaining.end());

    return totalTime;
}

int main() {
    int listLength;
    std::list<long> elements;

    std::cin >> listLength;

    for (int i = 0; i < listLength; i++) {
        long element;
        std::cin >> element;
        elements.push_back(element);
    }

    std::cout << solve(elements) << std::endl;

    return 0;
}