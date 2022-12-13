using System.IO;
using System.Text;

static class IO
{
    public static async Task<City> Read(TextReader input)
    {
        City city = new City();

        string[] firstLine = (await input.ReadLineAsync())!.Split(' ');
        int nodeCount = int.Parse(firstLine[0]);
        int edgeCount = int.Parse(firstLine[1]);

        for (int i = 0; i < nodeCount; i++)
        {
            string[] line = (await input.ReadLineAsync())!.Split(' ');
            int id = int.Parse(line[0]);
            float lat = float.Parse(line[1]);
            float lon = float.Parse(line[2]);

            city.AddNode(id, lat, lon);
        }

        for (int i = 0; i < edgeCount; i++)
        {
            string[] line = (await input.ReadLineAsync())!.Split(' ');
            int a = int.Parse(line[0]);
            int b = int.Parse(line[1]);
            long length = long.Parse(line[2]);

            if (a != b)
            {
                city.AddEdge(city.Nodes[a], city.Nodes[b], length);
            }
        }

        return city;
    }

    public static async Task<City> Read(string file)
    {
        using (StreamReader reader = new StreamReader(File.Open(file, FileMode.Open, FileAccess.Read), Encoding.UTF8))
        {
            return await Read(reader);
        }
    }

    public static async Task Write(IEnumerable<Node> path, TextWriter output)
    {
        output.WriteLine(Utils.GetPathLength(path));

        foreach (Node node in path)
        {
            await output.WriteLineAsync(node.Id.ToString());
        }
    }

    public static async Task Write(IEnumerable<Node> path, string file)
    {
        using (StreamWriter reader = new StreamWriter(File.Open(file, FileMode.Create, FileAccess.Write), Encoding.UTF8))
        {
            await Write(path, reader);
        }
    }
}