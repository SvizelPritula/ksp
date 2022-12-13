use text_io::read;

#[derive(Clone, Copy, Debug)]
enum JugId {
    A,
    B,
}

struct Jug {
    id: JugId,
    size: u64,
}

impl JugId {
    fn fill(&self) -> char {
        match self {
            JugId::A => 'A',
            JugId::B => 'B',
        }
    }

    fn empty(&self) -> char {
        match self {
            JugId::A => 'a',
            JugId::B => 'b',
        }
    }

    fn pour_in(&self) -> char {
        match self {
            JugId::A => '<',
            JugId::B => '>',
        }
    }
}

fn generate_sequence(small: Jug, large: Jug, target: u64) -> String {
    let mut seq = String::new();
    let mut content: u64 = 0;

    if target != 0 {
        seq.push(large.id.fill());
        content = large.size;
    }

    while content != target {
        if content > small.size {
            seq.push(small.id.pour_in());
            seq.push(small.id.empty());
            content -= small.size;
        } else {
            seq.push(small.id.pour_in());
            seq.push(large.id.fill());
            seq.push(small.id.pour_in());
            seq.push(small.id.empty());
            content = large.size - (small.size - content);
        }
    }

    seq
}

fn main() {
    let a: u64 = read!();
    let b: u64 = read!();
    let target: u64 = read!();

    let (small, large) = if a < b {
        (
            Jug {
                id: JugId::A,
                size: a,
            },
            Jug {
                id: JugId::B,
                size: b,
            },
        )
    } else {
        (
            Jug {
                id: JugId::B,
                size: b,
            },
            Jug {
                id: JugId::A,
                size: a,
            },
        )
    };

    let sequence = generate_sequence(small, large, target);
    let sequence = sequence.trim_end_matches(&['a', 'b']);

    println!("{length}", length = sequence.len());
    println!("{sequence}");
}
