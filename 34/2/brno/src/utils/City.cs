class Edge
{
    public Node A { get; set; }
    public Node B { get; set; }
    public long Length { get; set; }

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

    public float Lat { get; set; }
    public float Lon { get; set; }

    public int Id { get; set; }

    public Node(float lat, float lon, int id)
    {
        Lat = lat;
        Lon = lon;
        Id = id;
    }
}

class City
{
    public Dictionary<int, Node> NodesById { get; set; } = new Dictionary<int, Node>();
    public List<Node> Nodes { get; set; } = new List<Node>();
    public List<Edge> Edges { get; set; } = new List<Edge>();

    public Node AddNode(int id, float lat, float lon)
    {
        Node node = new Node(lat, lon, id);
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