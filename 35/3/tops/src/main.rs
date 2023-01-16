use std::io::stdin;

use anyhow::Result;
use solve::{solve, Lid};
use token_read::TokenReader;

mod solve;

fn main() -> Result<()> {
    let mut input = TokenReader::new(stdin().lock());

    let (case_count, radius): (usize, usize) = input.line()?;

    let mut cases = Vec::with_capacity(case_count);
    let mut lids = Vec::new();

    for (id, line) in input.take(case_count).enumerate() {
        let (weight, lid): (u64, u8) = line?;
        let lid = lid != 0;

        cases.push(weight);

        if lid {
            lids.push(Lid {
                id,
                start: id.saturating_sub(radius),
                end: id.saturating_add(radius).min(case_count - 1),
            });
        }
    }

    let placements = solve(&cases, lids);
    let weight: u64 = placements.iter().map(|(_, pos)| cases[*pos]).sum();

    println!("{weight}");

    for (id, pos) in placements {
        println!("{id} {pos}", id = id + 1, pos = pos + 1);
    }

    Ok(())
}
