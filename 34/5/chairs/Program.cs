using Chairs;

int[] firstLine = Console.ReadLine()!.Split().Select(s => int.Parse(s)).ToArray();

int customerCount = firstLine[0];
int chairCount = firstLine[1];

List<long> chairs = new List<long>(chairCount);

for (int i = 0; i < chairCount; i++) {
    long position = long.Parse(Console.ReadLine()!);
    chairs.Add(position);
}

(long MinDistance, List<int> Indices) = Solver.Solve(chairs, customerCount);

Console.WriteLine(MinDistance);

foreach (int index in Indices) {
    Console.WriteLine(index);
}
