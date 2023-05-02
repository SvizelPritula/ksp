use std::{
    cmp::{max, min},
    io::stdin,
};

use anyhow::Result;
use token_read::TokenReader;

fn get_hill_heights<I: Iterator<Item = u64>>(heights: I) -> impl Iterator<Item = u64> {
    heights.scan(0, |prev, curr| {
        *prev = max(*prev + 1, curr);
        Some(*prev)
    })
}

fn sand_volume(heights: &[u64]) -> u64 {
    let forward: Vec<u64> = get_hill_heights(heights.iter().copied()).collect();

    let mut backward: Vec<u64> = get_hill_heights(heights.iter().rev().copied()).collect();
    backward.reverse();
    let backward = backward;

    let mut sum: u64 = 0;

    for (i, height) in heights.iter().copied().enumerate() {
        let forward = forward[i];
        let backward = backward[i];

        let base = min(forward, backward);

        sum += (base - height) * 4;

        sum += if forward == backward { 1 } else { 2 };
    }

    sum
}

fn main() -> Result<()> {
    let mut input = TokenReader::new(stdin().lock());

    let (_height_count,): (usize,) = input.line()?;
    let heights: Vec<u64> = input.line()?;

    let volume = sand_volume(&heights);
    println!("{volume}");

    Ok(())
}
