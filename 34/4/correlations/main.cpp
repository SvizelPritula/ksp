#include <iostream>
#include <vector>
#include <queue>
#include <set>
#include <map>

struct correlation;

struct quantity
{
    int id;
    std::vector<correlation> correlations;
};

struct correlation
{
    int with;
    bool type;
};

struct metadata
{
    int parent;
    bool parity;
};

std::vector<int> walkToParent(int n, std::vector<quantity> quantities, std::map<int, metadata> meta)
{
    std::vector<int> result;
    result.push_back(n);

    while (meta.at(n).parent != -1)
    {
        n = meta.at(n).parent;
        result.push_back(n);
    }

    return result;
}

std::vector<int> unwind(int a, int b, std::vector<quantity> quantities, std::map<int, metadata> meta)
{
    std::vector<int> first = walkToParent(a, quantities, meta);
    std::vector<int> second = walkToParent(b, quantities, meta);

    std::vector<int> result;

    result.insert(result.end(), first.begin(), first.end());
    result.insert(result.end(), std::next(second.rbegin()), second.rend());
    result.push_back(*first.begin());

    return result;
}

std::vector<int> solve(std::vector<quantity> quantities)
{
    std::map<int, metadata> meta;
    std::set<int> unvisited;
    std::queue<int> queue;

    for (quantity &q : quantities)
    {
        unvisited.insert(q.id);
    }

    while (!unvisited.empty() || !queue.empty())
    {
        if (queue.empty())
        {
            int root = *unvisited.begin();
            meta[root] = {-1, false};
            queue.push(root);
            unvisited.erase(root);
        }

        int node = queue.front();
        queue.pop();

        int badNode = -1;

        for (correlation c : quantities.at(node).correlations)
        {
            if (unvisited.find(c.with) != unvisited.end())
            {
                queue.push(c.with);
                meta[c.with] = {node, meta.at(node).parity != c.type};
                unvisited.erase(c.with);
            }
            else
            {
                if (meta.at(c.with).parity != (meta.at(node).parity != c.type))
                    badNode = c.with;
            }
        }

        if (badNode >= 0)
            return unwind(node, badNode, quantities, meta);
    }

    throw std::logic_error("No contradiction found");
}

int main()
{
    int quantityCount, correlationCount;
    std::cin >> quantityCount >> correlationCount;

    std::vector<quantity> quantities;

    for (int i = 0; i < quantityCount; i++)
    {
        quantities.push_back({i});
    }

    for (int i = 0; i < correlationCount; i++)
    {
        int a, b, type;

        std::cin >> a >> b >> type;

        quantities.at(a).correlations.push_back({b, type < 0});
        quantities.at(b).correlations.push_back({a, type < 0});
    }

    std::vector<int> result = solve(quantities);

    std::cout << result.size() << std::endl;

    for (int i = 0; i < result.size(); i++)
    {
        if (i != 0)
            std::cout << ' ';
        std::cout << result.at(i);
    }

    std::cout << std::endl;

    return 0;
}