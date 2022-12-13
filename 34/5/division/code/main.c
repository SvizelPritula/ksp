#include <stdio.h>
#include <stdlib.h>

int sum_quotients_slow(int *array, int size, int max)
{
    int sum = 0;

    for (int i = 0; i < size; i++)
    {
        for (int j = 0; j < size; j++)
        {
            sum += array[i] / array[j];
        }
    }

    return sum;
}

void compute_prefix_sums(int *dest, int *array, int size)
{
    int sum = 0;

    for (int i = 0; i < size; i++)
    {
        sum += array[i];
        dest[i] = sum;
    }
}

void compute_histogram(int *dest, int *array, int size, int max)
{
    for (int i = 0; i <= max; i++)
    {
        dest[i] = 0;
    }

    for (int i = 0; i < size; i++)
    {
        dest[array[i]]++;
    }
}

int sum_quotients(int *array, int size, int max) {
    int *histogram = malloc((max + 1) * sizeof(int));
    int *histogram_prefix = malloc((max + 1) * sizeof(int));

    compute_histogram(histogram, array, size, max);
    compute_prefix_sums(histogram_prefix, histogram, max + 1);
    
    int sum = 0;

    for (int divisor = 1; divisor <= max; divisor++) {
        int divisor_count = histogram[divisor];

        for (int quotient = 0; quotient * divisor <= max; quotient++) {
            int start = quotient * divisor;
            int end = start + divisor - 1;

            if (end > max) end = max;

            int occurrences = histogram_prefix[end] - histogram_prefix[start];
            occurrences += histogram[start];

            sum += occurrences * quotient * divisor_count;
        }
    }

    free(histogram);
    free(histogram_prefix);

    return sum;
}

int main()
{
    int max = 1000;
    int array_size = max - rand() % (max / 10);

    int *array = malloc(array_size * sizeof(int));

    for (int i = 0; i < array_size; i++)
    {
        array[i] = 1 + rand() % max;
    }

    int sum = sum_quotients(array, array_size, max);

    printf("%d\n", sum);

    free(array);
    return 0;
}