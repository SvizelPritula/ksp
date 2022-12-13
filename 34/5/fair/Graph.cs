namespace Fair;

public record class Node(int Id)
{
    public List<Edge> Edges { get; } = new();
    public SortedList<long, Showcase> Showcases { get; set; } = new();

    public Showcase? GetLastShowcase(long time)
    {
        if (Showcases.Count == 0) return null;
        if (Showcases.Values[0].Start >= time) return null;

        int start = 0;
        int end = Showcases.Keys.Count - 1;

        while (start < end)
        {
            int middle = (start + end + 1) / 2;

            if (Showcases.Keys[middle] >= time)
            {
                end = middle - 1;
            }
            else
            {
                start = middle;
            }
        }

        return Showcases.Values[start];
    }
}

public record struct Edge(Node Destination, long Length);

public record class Graph
{
    public List<Node> Nodes { get; } = new();
    public List<Showcase> Showcases = new();
}

public record class Showcase(Node Room, long Start, long End);
