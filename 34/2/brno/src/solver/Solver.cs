using System.Drawing;

static class Solver
{
    static Random random = new Random();

    public static IEnumerable<Node> Solve(City city, TextWriter? logger = null)
    {
        logger ??= Console.Out;

        HashSet<Node> tree = CreateTree(city, random.Choose(city.Nodes));
        IEnumerable<Node> path = FindDiameter(city, tree);

        long lastLength = Utils.GetPathLength(path);

        long count = 0;

        logger.WriteLine($"Starting with {lastLength}");

        while (true)
        {
            tree = ExtendPath(city, path);
            IEnumerable<Node> newPath = FindDiameter(city, tree);

            long length = Utils.GetPathLength(newPath);

            logger.WriteLine($"{lastLength} => {length} (+{length - lastLength})");

            if (length <= lastLength)
            {
                count++;

                if (count >= 10) break;
                continue;
            }
            
            count = 0;

            path = newPath;
            lastLength = length;
        }

        return path;
    }

    private static HashSet<Node> CreateTree(City city, Node initial)
    {
        Dictionary<Node, long> distances = new Dictionary<Node, long>();
        PriorityQueue<Node, long> queue = new PriorityQueue<Node, long>();

        distances[initial] = 0;
        foreach (Edge edge in initial.Edges)
        {
            queue.Enqueue(edge.Other(initial), -edge.Length);
        }

        while (queue.Count > 0)
        {
            Node node = queue.Dequeue();
            if (distances.ContainsKey(node)) continue;

            int visitedNeighbourCount = node.Neighbours
                .Where(n => distances.ContainsKey(n))
                .Count();

            if (visitedNeighbourCount > 1) continue;

            Edge edge = node.Edges.Where(e => distances.ContainsKey(e.Other(node))).Single();
            Node neighbour = edge.Other(node);

            distances[node] = distances[neighbour] + edge.Length;

            foreach (Edge neighbourEdge in node.Edges)
            {
                queue.Enqueue(neighbourEdge.Other(node), -distances[node] - random.Next(1000));
            }
        }

        return new HashSet<Node>(distances.Keys);
    }

    private static HashSet<Node> ExtendPath(City city, IEnumerable<Node> oldPath)
    {
        Node first = oldPath.First();
        Node last = oldPath.Last();

        if (random.Next(2) == 0) oldPath = oldPath.Reverse();

        Dictionary<Node, long> distances = new();
        Dictionary<Node, Node> parents = new();

        PriorityQueue<Node, long> queue = new();

        long distance = 0;
        Node? lastNode = null;
        foreach (Node node in oldPath)
        {
            if (lastNode != null)
                distance += node.Edges.Where(e => e.Other(node) == lastNode).Single().Length;

            distances[node] = distance;
            parents[node] = node;

            foreach (Edge edge in node.Edges)
            {
                queue.Enqueue(edge.Other(node), -distance - random.Next(1000));
            }

            lastNode = node;
        }

        while (queue.Count > 0)
        {
            Node node = queue.Dequeue();
            if (distances.ContainsKey(node)) continue;

            int visitedNeighbourCount = node.Neighbours
                .Where(n => distances.ContainsKey(n))
                .Count();

            if (visitedNeighbourCount > 1) continue;

            Edge edge = node.Edges.Where(e => distances.ContainsKey(e.Other(node))).Single();
            Node neighbour = edge.Other(node);

            distances[node] = distances[neighbour] + edge.Length;
            parents[node] = parents[neighbour];

            foreach (Edge neighbourEdge in node.Edges)
            {
                queue.Enqueue(neighbourEdge.Other(node), -distances[node] - neighbourEdge.Length - random.Next(100));
            }
        }

        List<(Node node, Node pathNode, Node joinNode, long gain)> options = new();

        foreach (Node node in city.Nodes)
        {
            if (distances.ContainsKey(node)) continue;

            int visitedNeighbourCount = node.Neighbours
                .Where(n => distances.ContainsKey(n))
                .Count();

            if (visitedNeighbourCount != 2) continue;

            Edge? pathEdge = node.Edges
                .Where(e => distances.ContainsKey(e.Other(node)) && parents[e.Other(node)] == e.Other(node))
                .FirstOrDefault();

            if (pathEdge == null) continue;

            Edge? joinEdge = node.Edges
                .Where(e => distances.ContainsKey(e.Other(node)) && e.Other(node) != pathEdge.Other(node))
                .SingleOrDefault();

            if (joinEdge == null) continue;

            Node pathNode = pathEdge.Other(node);
            Node joinNode = joinEdge.Other(node);

            if (parents[joinNode] == pathNode) continue;
            if (pathNode.Neighbours.Contains(parents[joinNode])) continue;

            Node parentNode = parents[joinNode];

            long gain = (distances[joinNode] + pathEdge.Length + joinEdge.Length - distances[parentNode]) - Math.Abs(distances[pathNode] - distances[parentNode]);

            if (gain <= 0) continue;

            options.Add((node, pathNode, joinNode, gain));
        }

        IntervalContainer intervals = new();

        foreach ((Node node, Node pathNode, Node joinNode, long gain) in options.OrderByDescending(o => o.gain))
        {
            Node parentNode = parents[joinNode];

            if (parentNode == first || parentNode == last) continue;

            if (distances.ContainsKey(node)) continue;
            if (!distances.ContainsKey(pathNode) || !distances.ContainsKey(parentNode)) continue;

            long upperFence = Math.Max(distances[parentNode], distances[pathNode]);
            long lowerFence = Math.Min(distances[parentNode], distances[pathNode]);

            if (intervals.Test(lowerFence, upperFence)) continue;

            distances[node] = -1;
            parents[node] = parentNode;

            Node removedNode = parentNode.Neighbours
                .Where(n => distances.ContainsKey(n) && parents[n] == n)
                .Where(n => (distances[n] < distances[parentNode]) == (distances[pathNode] < distances[parentNode]))
                .Single();

            distances.Remove(removedNode);

            intervals.Add(lowerFence, upperFence);
        }

        return new HashSet<Node>(distances.Keys);
    }

    private static Dictionary<Node, (long distance, Node? parent)> ComputeDistances(City city, Node start, HashSet<Node> allowedNodes)
    {
        Dictionary<Node, (long distance, Node? parent)> distances = new Dictionary<Node, (long distance, Node? parent)>();
        Queue<Node> queue = new Queue<Node>();

        queue.Enqueue(start);
        distances[start] = (0, null);

        while (queue.Count > 0)
        {
            Node node = queue.Dequeue();

            foreach (Edge edge in node.Edges)
            {
                Node neighbour = edge.Other(node);

                if (distances.ContainsKey(neighbour)) continue;
                if (!allowedNodes.Contains(neighbour)) continue;

                distances[neighbour] = (distances[node].distance + edge.Length, node);
                queue.Enqueue(neighbour);
            }
        }

        return distances;
    }

    private static IEnumerable<Node> FindDiameter(City city, HashSet<Node> tree)
    {
        var distancesEnd = ComputeDistances(city, tree.First(), tree);
        Node end = distancesEnd.OrderByDescending(p => p.Value.distance).Select(p => p.Key).First();

        var distances = ComputeDistances(city, end, tree);
        Node start = distances.OrderByDescending(p => p.Value.distance).Select(p => p.Key).First();

        Node node = start;

        yield return node;

        while (distances[node].parent != null)
        {
            node = distances[node].parent!;
            yield return node;
        }
    }
}