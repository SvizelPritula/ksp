use std::{io::stdin, process::ExitCode};

use anyhow::Result;
use solve::{solve, Solution};
use token_read::TokenReader;

mod solve;

fn main() -> Result<ExitCode> {
    let mut input = TokenReader::new(stdin().lock());

    let _lengths: (usize, usize) = input.line()?;
    let a: String = input.line_raw()?;
    let b: String = input.line_raw()?;

    if let Some(Solution {
        delta,
        offset,
        start,
        end,
    }) = solve(a.as_bytes(), b.as_bytes())
    {
        println!("{delta} {offset} {start} {end}");

        Ok(ExitCode::SUCCESS)
    } else {
        Ok(ExitCode::FAILURE)
    }
}
