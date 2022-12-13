using System.Threading.Channels;

Channel<IEnumerable<Node>> channel = Channel.CreateUnbounded<IEnumerable<Node>>();
City city = await IO.Read("input.txt");

void Run()
{
    FileStream file = File.OpenWrite($"log/{Guid.NewGuid()}.txt");
    StreamWriter log = new StreamWriter(file);
    log.AutoFlush = true;

    while (true)
    {
        IEnumerable<Node> solution = Solver.Solve(city, log);

        channel.Writer.WriteAsync(solution).AsTask().Wait();
    }
}

await Task.Run(() => Directory.CreateDirectory("output/"));
await Task.Run(() => Directory.CreateDirectory("image/"));
await Task.Run(() => Directory.CreateDirectory("log/"));

string token = await File.ReadAllTextAsync("token.txt");
API api = new API(token.Trim());

long best = await api.GetPathLength();
long bestOffline = -1;

for (int i = 0; i < Environment.ProcessorCount; i++)
{
    Thread thread = new Thread(Run);
    thread.Start();
}

while (true)
{
    IEnumerable<Node> solution = await channel.Reader.ReadAsync();
    long length = Utils.GetPathLength(solution);

    if (length > bestOffline)
    {
        Console.WriteLine();
        Console.WriteLine("====== New record! ======");
        Console.WriteLine($"{DateTime.Now.ToShortTimeString()} Found path with length {length}");
        bestOffline = length;

        await IO.Write(solution, $"output/{length}.txt");
        await File.WriteAllTextAsync($"image/{length}.svg", Visualize.GraphToSvg(city, Utils.NodePathToEdgeList(solution)));

        if (length > best)
        {
            best = length;
            Console.WriteLine("Uploading...");

            string verdict = await api.Upload(solution);

            Console.WriteLine(verdict);
        }

        Console.WriteLine();
    }
    else if (length > 1000000)
    {
        Console.WriteLine($"{DateTime.Now.ToShortTimeString()} Found path with length {length}");
    }
}