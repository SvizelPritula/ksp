use std::collections::BTreeMap;

use text_io::scan;

fn count_valid_positions(
    positions: Vec<u64>,
    circle_size: u64,
    window_size: u64,
    target_count: isize,
) -> u64 {
    let mut deltas = BTreeMap::new();
    let mut initial_count = 0isize;

    for position in positions {
        let start = position;
        let end = position + window_size;

        *deltas.entry(start).or_insert(0isize) += 1;
        *deltas.entry(end % circle_size).or_insert(0isize) -= 1;

        if end >= circle_size {
            initial_count += 1;
        }
    }

    let mut count = initial_count;
    let mut last_pos = 0;
    let mut valid_positions = 0;

    for (pos, delta) in deltas {
        if count == target_count {
            valid_positions += pos - last_pos;
        }

        count += delta;
        last_pos = pos;
    }

    if count == target_count {
        valid_positions += circle_size - last_pos;
    }

    valid_positions
}

fn main() {
    let circle_size: u64;
    let organizer_count: usize;
    let window_size: u64;
    let target_count: isize;

    scan!(
        "{} {} {} {}",
        circle_size,
        organizer_count,
        window_size,
        target_count
    );

    let mut positions = Vec::with_capacity(organizer_count);

    for _ in 0..organizer_count {
        let position: u64;
        scan!("{}", position);

        positions.push(position - 1);
    }

    positions.sort();

    let valid_positions = count_valid_positions(positions, circle_size, window_size, target_count);
    println!("{valid_positions}");
}
