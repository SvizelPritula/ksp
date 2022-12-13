use std::io::{self, BufRead};

use anyhow::{anyhow, bail, Result};
use num::BigRational;
use vector::Vector;

use crate::solve::solve;

mod eliminate;
mod solve;
mod vector;

fn main() -> Result<()> {
    let input = io::stdin().lock();
    let mut input = input.lines();

    let row_count: usize = input
        .next()
        .ok_or_else(|| anyhow!("expected row count"))??
        .trim()
        .parse()?;

    let mut equations = Vec::with_capacity(row_count);

    for _ in 0..row_count {
        let equation = input
            .next()
            .ok_or_else(|| anyhow!("expected equation"))??
            .split_whitespace()
            .map(|s| s.parse())
            .collect::<Result<Vector<BigRational>, _>>()?;

        if equation.len() != row_count + 1 {
            bail!("expected {len} elements", len = row_count + 1);
        }

        equations.push(equation);
    }

    match solve(equations) {
        solve::Solution::None => {
            println!("N");
        }
        solve::Solution::Single(values) => {
            println!("J");

            println!(
                "{}",
                values
                    .into_iter()
                    .map(|v| v.to_string())
                    .collect::<Vec<_>>()
                    .join(" ")
            );
        }
        solve::Solution::Multiple(values) => {
            println!("P");

            println!(
                "{}",
                values
                    .iter()
                    .map(|v| v[values.len()].to_string())
                    .collect::<Vec<_>>()
                    .join(" ")
            );

            for parameter in 0..values.len() {
                println!(
                    "{}",
                    values
                        .iter()
                        .map(|v| v[parameter].to_string())
                        .collect::<Vec<_>>()
                        .join(" ")
                );
            }
        }
    }

    Ok(())
}
