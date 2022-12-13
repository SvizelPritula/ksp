using Fair;

string[] firstLine = Console.ReadLine()!.Split();

int nodeCount = int.Parse(firstLine[0]);
int edgeCount = int.Parse(firstLine[1]);
int showcaseCount = int.Parse(firstLine[2]);

Graph graph = new();

for (int node = 0; node < nodeCount; node++)
{
    graph.Nodes.Add(new Node(node));
}

for (int edge = 0; edge < edgeCount; edge++)
{
    string[] line = Console.ReadLine()!.Split();

    int a = int.Parse(line[0]);
    int b = int.Parse(line[1]);
    long length = long.Parse(line[2]);

    graph.Nodes[a].Edges.Add(new Edge(graph.Nodes[b], length));
}

Dictionary<Node, List<Showcase>> showcaseMap = new();

foreach (Node node in graph.Nodes)
{
    showcaseMap[node] = new();
}

for (int showcase = 0; showcase < showcaseCount; showcase++)
{
    string[] line = Console.ReadLine()!.Split();

    int nodeId = int.Parse(line[0]);
    long start = long.Parse(line[1]);
    long length = long.Parse(line[2]);

    Node node = graph.Nodes[nodeId];

    Showcase newShowcase = new Showcase(node, start, start + length);

    graph.Showcases.Add(newShowcase);
    showcaseMap[node].Add(newShowcase);
}

foreach (Node node in graph.Nodes)
{
    node.Showcases = new SortedList<long, Showcase>(showcaseMap[node].ToDictionary(s => s.Start));
}

(long score, List<IInstruction> instructions) = Solver.Solve(graph);

Console.WriteLine(score);

foreach (IInstruction instruction in instructions)
{
    Console.WriteLine(instruction.ToString());
}