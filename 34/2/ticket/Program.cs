static Dictionary<Node, long> DijkstrasAlgorithm(Graph graph, Node start)
{
    Dictionary<Node, long> distances = new Dictionary<Node, long>();
    Dictionary<Node, long> counts = new Dictionary<Node, long>();
    PriorityQueue<Node, long> queue = new PriorityQueue<Node, long>();

    distances[start] = 0;
    queue.Enqueue(start, 0);

    while (queue.Count > 0)
    {
        Node node = queue.Dequeue();

        foreach (Edge edge in node.Edges)
        {
            Node neighbour = edge.Other(node);
            long distance = distances[node] + edge.Length;

            if (distances.ContainsKey(neighbour) && distances[neighbour] <= distance) continue;

            distances[neighbour] = distance;
            queue.Enqueue(neighbour, distances[neighbour]);
        }
    }

    return distances;
}

static long Solve(Graph graph)
{
    Dictionary<Node, long> a = DijkstrasAlgorithm(graph, graph.NodesById[1]);
    Dictionary<Node, long> b = DijkstrasAlgorithm(graph, graph.NodesById[2]);
    Dictionary<Node, long> c = DijkstrasAlgorithm(graph, graph.NodesById[3]);

    long minCost = long.MaxValue;

    foreach (Node node in graph.Nodes)
    {
        long cost = 0;

        cost += a[node] * graph.SingleCost;
        cost += b[node] * graph.SingleCost;
        cost += c[node] * graph.GroupCost;

        minCost = Math.Min(minCost, cost);
    }

    return minCost;
}

static int[] ReadLine()
{
    return Console.ReadLine()!.Split(' ').Select(n => int.Parse(n)).ToArray(); ;
}

static Graph Parse()
{
    int[] header = ReadLine();

    int nodeCount = header[0];
    int edgeCount = header[1];
    int singleCost = header[2];
    int groupCost = header[3];

    Graph graph = new Graph(singleCost, groupCost);

    for (int i = 1; i <= nodeCount; i++)
    {
        graph.AddNode(i);
    }

    for (int i = 0; i < edgeCount; i++)
    {
        int[] line = ReadLine();

        int a = line[0];
        int b = line[1];
        int length = line[2];

        graph.AddEdge(graph.NodesById[a], graph.NodesById[b], length);
    }

    return graph;
}

Graph graph = Parse();
long solution = Solve(graph);
Console.WriteLine(solution);