public static class RandomEx
{
    public static T Choose<T>(this Random random, IList<T> list)
    {
        if (list.Count <= 0)
        {
            throw new IndexOutOfRangeException("Cannot choose from empty list");
        }

        return list[(int)Math.Floor(random.NextDouble() * list.Count)];
    }

    public static IList<T> Shuffle<T>(this Random random, IList<T> list)  
{
        list = list.ToList();
        int n = list.Count;
        while (n > 1)
        {
            n--;
            int k = random.Next(n + 1);
            T value = list[k];
            list[k] = list[n];
            list[n] = value;
        }
        return list;
    }
    }