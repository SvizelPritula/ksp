use std::{
    error,
    io::{stdin, BufRead, Lines, StdinLock},
    str::FromStr,
};

use anyhow::{anyhow, Error, Result};
use solver::{get_start_times, Dependency};

mod solver;

fn main() -> Result<()> {
    let input = stdin().lock();
    let mut lines = input.lines();

    let [potion_count, dependency_count]: [usize; 2] = read_line(&mut lines)?;

    let preparation_times: Vec<u64> = read_line_vec(&mut lines)?;
    if preparation_times.len() != potion_count {
        Err(anyhow!(
            "Expected {potion_count} numbers, got {real}",
            real = preparation_times.len()
        ))?
    }

    let mut dependencies: Vec<Dependency> = Vec::new();

    for _ in 0..dependency_count {
        let [dependency, dependant]: [usize; 2] = read_line(&mut lines)?;
        dependencies.push(Dependency {
            dependant: dependant - 1,
            dependency: dependency - 1,
        })
    }

    let start_times = get_start_times(preparation_times, dependencies)?;

    println!(
        "{}",
        start_times
            .iter()
            .map(|t| t.to_string())
            .collect::<Vec<String>>()
            .join(" ")
    );

    Ok(())
}

fn read_line_vec<T>(lines: &mut Lines<StdinLock>) -> Result<Vec<T>>
where
    T: FromStr,
    T::Err: error::Error + Send + Sync + 'static,
{
    Ok(lines
        .next()
        .ok_or(Error::msg("Unexpected EOF"))??
        .split_whitespace()
        .map(|t| t.parse::<T>())
        .collect::<Result<Vec<T>, T::Err>>()?)
}

fn read_line<T, const N: usize>(lines: &mut Lines<StdinLock>) -> Result<[T; N]>
where
    T: FromStr,
    T::Err: error::Error + Send + Sync + 'static,
{
    let vec = read_line_vec(lines)?;
    Ok(<[T; N]>::try_from(vec).or(Err(Error::msg("Unexpected EOF")))?)
}
