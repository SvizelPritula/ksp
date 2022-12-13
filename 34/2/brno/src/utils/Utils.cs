static class Utils
{
    public static IEnumerable<Edge> NodePathToEdgeList(IEnumerable<Node> path)
    {
        Node lastNode = path.First();

        foreach (Node nextNode in path.Skip(1))
        {
            yield return lastNode.Edges.Where(e => e.Other(lastNode) == nextNode).Single();

            lastNode = nextNode;
        }
    }

    public static long GetPathLength(IEnumerable<Node> path)
    {
        return NodePathToEdgeList(path).Select(e => e.Length).Sum();
    }
}