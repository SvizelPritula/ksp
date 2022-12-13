using System;
using System.Runtime.InteropServices;

public class IntervalContainer
{
    [DllImport("libinterval.so")]
    static extern IntPtr create_interval_container();
    [DllImport("libinterval.so")]
    static extern void free_interval_container(IntPtr container);
    [DllImport("libinterval.so")]
    static extern void add_interval(IntPtr container, long start, long end);
    [DllImport("libinterval.so")]
    static extern bool test_interval(IntPtr container, long start, long end);

    IntPtr pointer;

    public IntervalContainer()
    {
        pointer = create_interval_container();
    }

    ~IntervalContainer()
    {
        free_interval_container(pointer);
    }

    public void Add(long start, long end)
    {
        add_interval(pointer, start, end);
        GC.KeepAlive(this);
    }

    public bool Test(long start, long end)
    {
        bool result = test_interval(pointer, start, end);
        GC.KeepAlive(this);
        return result;
    }
}