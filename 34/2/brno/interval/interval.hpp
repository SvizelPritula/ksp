extern "C"
{
    void *create_interval_container();
    void free_interval_container(void *container);
    void add_interval(void *container, long start, long end);
    bool test_interval(void *container, long start, long end);
}