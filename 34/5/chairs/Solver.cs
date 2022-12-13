namespace Chairs;

public static class Solver
{
    private static List<int>? SelectChairs(List<long> positions, long minDistance, int customerCount)
    {
        long lastPosition = positions.First();

        List<int> indices = new List<int>(customerCount);
        indices.Add(0);

        foreach ((long position, int index) in positions.Select((p, i) => (p, i)).Skip(1))
        {
            if (position - lastPosition >= minDistance)
            {
                indices.Add(index);
                lastPosition = position;
            }

            if (indices.Count >= customerCount) break;
        }

        if (indices.Count >= customerCount)
        {
            return indices;
        }
        else
        {
            return null;
        }
    }

    public static (long MinDistance, List<int> Indices) Solve(List<long> positions, int customerCount)
    {
        long start = 0;
        long end = positions.Last();

        while (start != end)
        {
            long middle = (start + end + 1) / 2;

            List<int>? indices = SelectChairs(positions, middle, customerCount);

            if (indices == null)
            {
                end = middle - 1;
            }
            else
            {
                start = middle;
            }
        }

        return (start, SelectChairs(positions, start, customerCount)!);
    }
}