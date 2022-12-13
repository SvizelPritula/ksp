namespace Fair;

public record struct NodePair(Node From, Node To)
{
    public override int GetHashCode()
    {
        return (From, To).GetHashCode();
    }
}

public record struct DistanceInfo(long Distance, Node Next);
public record struct ShowcaseInfo(long Score, InstructionLink Path);

public record class InstructionLink(IInstruction Instruction, InstructionLink? Nextious);

public static class Solver
{
    private static Dictionary<NodePair, DistanceInfo> CalculateDistances(Graph graph)
    {
        Dictionary<NodePair, DistanceInfo> distances = new();

        bool Connection(Node a, Node b)
        {
            return distances.ContainsKey(new NodePair(a, b));
        }

        long Distance(Node a, Node b)
        {
            return distances[new NodePair(a, b)].Distance;
        }

        Node Next(Node a, Node b)
        {
            return distances[new NodePair(a, b)].Next;
        }

        foreach (Node node in graph.Nodes)
        {
            distances[new NodePair(node, node)] = new DistanceInfo(0, node);

            foreach (Edge edge in node.Edges)
            {
                distances[new NodePair(node, edge.Destination)] = new DistanceInfo(edge.Length, edge.Destination);
            }
        }

        foreach (Node k in graph.Nodes)
        {
            foreach (Node i in graph.Nodes)
            {
                foreach (Node j in graph.Nodes)
                {
                    if (!Connection(i, k) || !Connection(k, j)) continue;
                    if (!Connection(i, j) || (Distance(i, j) > Distance(i, k) + Distance(k, j)))
                    {
                        distances[new NodePair(i, j)] = new DistanceInfo(
                            Distance(i, k) + Distance(k, j),
                            Next(i, k)
                        );
                    }
                }
            }
        }

        return distances;
    }

    public static (long Score, List<IInstruction> Instructions) Solve(Graph graph)
    {
        Dictionary<NodePair, DistanceInfo> distances = CalculateDistances(graph);

        bool Connection(Node a, Node b)
        {
            return distances.ContainsKey(new NodePair(a, b));
        }

        long Distance(Node a, Node b)
        {
            return distances[new NodePair(a, b)].Distance;
        }

        Node Next(Node a, Node b)
        {
            return distances[new NodePair(a, b)].Next;
        }

        Dictionary<Showcase, ShowcaseInfo> showcaseInfos = new();

        foreach (Showcase showcase in graph.Showcases.OrderBy(s => s.Start))
        {
            Node dest = showcase.Room;

            foreach (Node node in graph.Nodes)
            {
                if (!Connection(node, dest)) continue;

                long leaveTime = showcase.Start - Distance(node, dest);
                Showcase? NextiousShowcase = node.GetLastShowcase(leaveTime);

                ShowcaseInfo showcaseInfo;

                if (NextiousShowcase == null)
                {
                    if (leaveTime < 0) continue;
                    if (node != graph.Nodes[0]) continue;

                    showcaseInfo = new ShowcaseInfo(0, new InstructionLink(new WaitInstruction(leaveTime), null));
                }
                else
                {
                    if (!showcaseInfos.ContainsKey(NextiousShowcase)) continue;

                    showcaseInfo = showcaseInfos[NextiousShowcase];
                    showcaseInfo.Score += Math.Min(NextiousShowcase.End, leaveTime) - NextiousShowcase.Start;
                    showcaseInfo.Path = new InstructionLink(new WaitInstruction(leaveTime - NextiousShowcase.Start), showcaseInfo.Path);
                }

                for (Node subnode = node; subnode != dest; subnode = Next(subnode, dest))
                {
                    showcaseInfo.Path = new InstructionLink(new MoveInstruction(Next(subnode, dest)), showcaseInfo.Path);
                }

                if (!showcaseInfos.ContainsKey(showcase) || showcaseInfos[showcase].Score < showcaseInfo.Score)
                {
                    showcaseInfos[showcase] = showcaseInfo;
                }
            }
        }

        ShowcaseInfo best = showcaseInfos
            .Select(pair =>
            {
                (Showcase showcase, ShowcaseInfo showcaseInfo) = pair;

                long duration = showcase.End - showcase.Start;
                showcaseInfo.Score += duration;
                showcaseInfo.Path = new InstructionLink(new WaitInstruction(duration), showcaseInfo.Path);

                return showcaseInfo;
            }).MaxBy(s => s.Score);

        return (best.Score, MinimizeInstructions(UnwindInstructions(best.Path)));
    }

    private static List<IInstruction> UnwindInstructions(InstructionLink end)
    {
        List<IInstruction> instructions = new();

        for (InstructionLink? link = end; link != null; link = link.Nextious)
        {
            instructions.Add(link.Instruction);
        }

        instructions.Reverse();
        return instructions;
    }

    private static List<IInstruction> MinimizeInstructions(List<IInstruction> instructions)
    {
        List<IInstruction> optimized = new();

        foreach (IInstruction instruction in instructions)
        {
            if (instruction is WaitInstruction wait)
            {
                if (wait.Time == 0) continue;

                if (optimized.Count > 0 && optimized[optimized.Count - 1] is WaitInstruction previous)
                {
                    optimized[optimized.Count - 1] = new WaitInstruction(previous.Time + wait.Time);
                    continue;
                }
            }

            optimized.Add(instruction);
        }

        return optimized;
    }
}
