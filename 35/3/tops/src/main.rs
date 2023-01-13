use std::{collections::BTreeSet, io::stdin};

use anyhow::Result;
use token_read::TokenReader;

fn main() -> Result<()> {
    let mut input = TokenReader::new(stdin().lock());

    let (case_count, radius): (usize, usize) = input.line()?;

    let mut cases = Vec::with_capacity(case_count);
    let mut lids = BTreeSet::new();

    for (id, line) in input.take(case_count).enumerate() {
        let (weight, lid): (u64, u8) = line?;
        let lid = lid != 0;

        cases.push(weight);

        if lid {
            lids.insert(id);
        }
    }

    println!("{radius:?} {cases:?} {lids:?}");

    Ok(())
}
