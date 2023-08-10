#include <iostream>
#include <string>
#include <optional>

bool has_single_error(std::string corrupted, std::string reference)
{
    if (corrupted.length() != reference.length() + 1)
        return false;

    auto c = corrupted.begin();
    auto r = reference.begin();

    while (r < reference.end())
    {
        if (*c != *r)
            return std::equal(c + 1, corrupted.end(), r);

        c++;
        r++;
    }

    return true;
}

std::string impossible = "[chyba]";
std::string ambiguous = "[neunikatni]";

std::string solve(std::string trans)
{
    size_t len = trans.length();

    if (len % 2 != 1)
        return impossible;

    std::string first_c = trans.substr(0, len / 2 + 1);
    std::string first_r = trans.substr(len / 2 + 1, len);

    std::string second_c = trans.substr(len / 2, len);
    std::string second_r = trans.substr(0, len / 2);

    bool first = has_single_error(first_c, first_r);
    bool second = has_single_error(second_c, second_r);

    if (first && second && first_r != second_r)
        return ambiguous;
    else if (first)
        return first_r;
    else if (second)
        return second_r;
    else
        return impossible;
}

int main()
{
    uint64_t transmission_count;
    std::cin >> transmission_count;

    for (uint64_t i = 0; i < transmission_count; i++)
    {
        size_t _length;
        std::string transmission;

        std::cin >> _length >> transmission;

        std::cout << solve(transmission) << std::endl;
    }
}
