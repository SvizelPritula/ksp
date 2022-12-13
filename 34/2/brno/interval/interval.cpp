#include <set>

#include <interval.hpp>

struct interval
{
    long start;
    long end;
};

bool operator<(interval a, interval b)
{
    return a.start < b.start;
}

void *create_interval_container()
{
    return new std::set<interval>();
}

void free_interval_container(void *p)
{
    std::set<interval> *container = (std::set<interval> *)p;
    delete container;
}

void add_interval(void *p, long start, long end)
{
    std::set<interval> *container = (std::set<interval> *)p;
    container->insert({start, end});
}

bool test_interval(void *p, long start, long end)
{
    std::set<interval> *container = (std::set<interval> *)p;

    auto next_interval = container->lower_bound({start, 0});
    if (next_interval != container->end())
    {
        if (next_interval->start <= end)
            return true;
    }

    if (next_interval != container->begin())
    {
        auto prev_interval = next_interval;
        prev_interval--;
        
        if (prev_interval->end >= start)
            return true;
    }

    return false;
}