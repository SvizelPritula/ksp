using System.Drawing;
using System.Xml.Linq;

static class Visualize
{
    private static int size = 1024 * 4;

    public static string GraphToSvg(City city, Dictionary<Edge, Color> colors)
    {
        float minLat = city.Nodes.Select(n => n.Lat).Min();
        float maxLat = city.Nodes.Select(n => n.Lat).Max();
        float minLon = city.Nodes.Select(n => n.Lon).Min();
        float maxLon = city.Nodes.Select(n => n.Lon).Max();

        Func<float, float> latToX = (lat) => ((lat - minLat) / (maxLat - minLat)) * size;
        Func<float, float> lonToY = (lon) => ((lon - minLon) / (maxLon - minLon)) * size;

        XNamespace ns = "http://www.w3.org/2000/svg";

        XElement svg = new XElement(
            ns + "svg",
            new XAttribute("width", size),
            new XAttribute("height", size),
            city.Edges.Select(e => new XElement(
                ns + "line",
                new XAttribute("x1", latToX(e.A.Lat)),
                new XAttribute("y1", lonToY(e.A.Lon)),
                new XAttribute("x2", latToX(e.B.Lat)),
                new XAttribute("y2", lonToY(e.B.Lon)),
                new XAttribute("stroke", ColorTranslator.ToHtml(colors.GetValueOrDefault(e, Color.Black)).ToLowerInvariant()),
                new XAttribute("stroke-width", 1)
            ))
        );

        return svg.ToString();
    }

    public static string GraphToSvg(City city, Dictionary<Color, IEnumerable<Edge>> colors)
    {
        Dictionary<Edge, Color> colorTable = new Dictionary<Edge, Color>();

        foreach (var pair in colors)
        {
            foreach (Edge e in pair.Value)
            {
                colorTable[e] = pair.Key;
            }
        }

        return GraphToSvg(city, colorTable);
    }

    public static string GraphToSvg(City city, IEnumerable<Edge> highlight)
    {
        return GraphToSvg(city, new Dictionary<Color, IEnumerable<Edge>>{
            {Color.Red, highlight}
        });
    }
}