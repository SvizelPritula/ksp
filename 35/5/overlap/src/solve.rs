use std::ops::RangeInclusive;

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
pub struct Solution {
    pub delta: isize,
    pub offset: isize,
    pub start: usize,
    pub end: usize,
}

fn best_delta<I: Iterator<Item = isize>>(deltas: I) -> Option<(RangeInclusive<usize>, isize)> {
    let mut start = 0usize;
    let mut delta = 0isize;

    let mut best: Option<(RangeInclusive<usize>, isize)> = None;

    for (i, value) in deltas.enumerate() {
        if delta <= 0 {
            delta = 0;
            start = i;
        }

        delta += value;

        let is_better = match &best {
            Some((_r, d)) => *d < delta,
            None => true,
        };

        if is_better {
            best = Some((start..=i, delta));
        }
    }

    best
}

pub fn solve(a: &[u8], b: &[u8]) -> Option<Solution> {
    let a_size = a.len() as isize;
    let b_size = b.len() as isize;

    let offsets = -a_size..=b_size;

    offsets
        .filter_map(|offset| {
            let deltas = a.iter().copied().enumerate().map(|(i, a)| {
                if let Some(b) = i.checked_add_signed(offset).and_then(|i| b.get(i)).copied() {
                    if a == b {
                        2
                    } else {
                        -2
                    }
                } else {
                    -1
                }
            });

            best_delta(deltas).map(|(range, delta)| Solution {
                delta,
                offset,
                start: *range.start(),
                end: *range.end(),
            })
        })
        .max_by_key(|s| s.delta)
}
