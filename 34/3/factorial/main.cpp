#include <iostream>
#include <vector>
#include <limits>

std::vector<std::pair<unsigned long long, unsigned long long>> factorize(unsigned long long n)
{
    std::vector<std::pair<unsigned long long, unsigned long long>> result;

    for (unsigned long long i = 2; i * i <= n && n > 1; i++)
    {
        unsigned long long count = 0;

        while (n % i == 0)
        {
            count++;
            n /= i;
        }

        if (count > 1)
        {
            result.push_back({i, count});
        }
    }

    if (n > 1)
    {
        result.push_back({n, 1});
    }

    return result;
}

unsigned long long countZeroes(unsigned long long number, unsigned long long base)
{
    std::vector<std::pair<unsigned long long, unsigned long long>> factors = factorize(base);

    unsigned long long zeroes = std::numeric_limits<unsigned long long>::max();

    for (std::pair<unsigned long long, unsigned long long> entry : factors)
    {
        unsigned long long factor = entry.first;
        unsigned long long count = entry.second;

        unsigned long long divident = factor;
        unsigned long long occurrences = 0;

        while (true)
        {
            occurrences += number / divident;

            if (std::numeric_limits<unsigned long long>::max() / factor < divident)
                break;
            divident *= factor;
        }

        zeroes = std::min(zeroes, occurrences / count);
    }

    return zeroes;
}

int main()
{
    unsigned long long number;
    unsigned long long base;

    std::cin >> number >> base;

    std::cout << countZeroes(number, base) << std::endl;

    return 0;
}