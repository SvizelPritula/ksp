fn join(counts: &Vec<u32>) -> String {
    counts
        .iter()
        .map(|n| format!("{}", n))
        .collect::<Vec<_>>()
        .join(" ")
}

fn product(counts: &Vec<u32>, primes: &Vec<u32>) -> u32 {
    counts
        .iter()
        .enumerate()
        .map(|(i, v)| primes[i].pow(*v))
        .product::<u32>()
}

fn main() {
    let primes: Vec<u32> = vec![2, 3, 7, 11, 13];
    let limit = 20;

    let mut counts = vec![0; primes.len()];

    'search: loop {
        println!(
            "{p:02} - {c}",
            c = join(&counts),
            p = product(&counts, &primes)
        );

        let mut i = 0;
        counts[i] += 1;

        while product(&counts, &primes) > limit {
            if i >= primes.len() - 1 {
                break 'search;
            }

            counts[i] = 0;
            i += 1;
            counts[i] += 1;
        }
    }
}
