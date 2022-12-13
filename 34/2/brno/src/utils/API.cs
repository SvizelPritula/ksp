using System.Net.Http.Headers;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;

class API
{
    private static Uri baseUri = new Uri("https://ksp.mff.cuni.cz/api/");
    private static string taskName = "34-2-4";

    private readonly HttpClient client;

    public API(string token)
    {
        client = new HttpClient();
        client.BaseAddress = baseUri;
        client.DefaultRequestHeaders.Authorization = new AuthenticationHeaderValue("Bearer", token);
        client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("brno-walker", "0.1"));
        client.DefaultRequestHeaders.UserAgent.Add(new ProductInfoHeaderValue("(like Gecko)"));
    }

    public async Task<string> GetStatusString()
    {
        HttpResponseMessage res = await client.GetAsync($"tasks/status?task={Uri.EscapeDataString(taskName)}");

        if (((int)res.StatusCode) != 200)
        {
            throw new Exception($"Unexpected status code of {res.StatusCode}");
        }

        string str = await res.Content.ReadAsStringAsync();
        JsonDocument response = JsonDocument.Parse(str);

        foreach (JsonElement subtask in response.RootElement.GetProperty("subtasks").EnumerateArray())
        {
            if (subtask.GetProperty("input_generated").GetBoolean())
            {
                string? verdict = subtask.GetProperty("verdict").GetString();

                if (verdict == null)
                {
                    throw new Exception("No verdict found");
                }

                return verdict;
            }
        }

        throw new Exception("No valid subtask");
    }

    public async Task<int> GetPathLength()
    {
        string verdict = await GetStatusString();

        Match match = Regex.Match(verdict, "(\\d+)m");

        if (!match.Success) return -1;

        return int.Parse(match.Groups[1].Value);
    }

    public async Task<string> Upload(IEnumerable<Node> path)
    {
        StringBuilder builder = new StringBuilder();
        await IO.Write(path, new StringWriter(builder));

        string content = builder.ToString();

        HttpRequestMessage req = new HttpRequestMessage(HttpMethod.Post, $"tasks/submit?task={Uri.EscapeDataString(taskName)}&subtask=1");
        req.Content = new StringContent(content, System.Text.Encoding.UTF8);
        req.Content.Headers.ContentType = new MediaTypeHeaderValue("text/plain");

        HttpResponseMessage res = await client.SendAsync(req);


        if (((int)res.StatusCode) != 200)
        {
            throw new Exception($"Unexpected status code of {res.StatusCode}");
        }

        string str = await res.Content.ReadAsStringAsync();
        JsonDocument response = JsonDocument.Parse(str);

        string? verdict = response.RootElement.GetProperty("verdict").GetString();

        if (verdict == null)
        {
            throw new Exception("No verdict found");
        }

        return verdict;
    }
}