class Edge
{
    public Node A { get; }
    public Node B { get; }
    public long Length { get; }

    public Edge(Node a, Node b, long length)
    {
        A = a;
        B = b;
        Length = length;

        A.Edges.Add(this);
        B.Edges.Add(this);
    }

    public Node Other(Node node)
    {
        if (A == node)
        {
            return B;
        }
        else if (B == node)
        {
            return A;
        }
        else
        {
            throw new KeyNotFoundException("Node not part of edge");
        }
    }
}

class Node
{
    public List<Edge> Edges { get; set; } = new List<Edge>();

    public IEnumerable<Node> Neighbours => Edges.Select(e => e.Other(this));

    public int Id { get; set; }

    public Node(int id)
    {
        Id = id;
    }

    public override int GetHashCode()
    {
        return Id;
    }

}

class Graph
{
    public Dictionary<int, Node> NodesById { get; } = new Dictionary<int, Node>();
    public List<Node> Nodes { get; } = new List<Node>();
    public List<Edge> Edges { get; } = new List<Edge>();

    public int SingleCost { get; }
    public int GroupCost { get; }

    public Graph(int singleCost, int groupCost)
    {
        SingleCost = singleCost;
        GroupCost = groupCost;
    }

    public Node AddNode(int id)
    {
        Node node = new Node(id);
        NodesById.Add(id, node);
        Nodes.Add(node);
        return node;
    }

    public Edge AddEdge(Node a, Node b, long length)
    {
        Edge edge = new Edge(a, b, length);
        Edges.Add(edge);
        return edge;
    }
}