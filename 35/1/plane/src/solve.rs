use crate::sparse::ShiftableSparseArray;
use anyhow::{anyhow, Error};

pub enum Command {
    Up,
    Down,
    Unknown,
}

impl TryFrom<char> for Command {
    type Error = Error;

    fn try_from(value: char) -> Result<Self, Self::Error> {
        match value {
            '^' => Ok(Command::Up),
            'v' => Ok(Command::Down),
            '?' => Ok(Command::Unknown),
            c => Err(anyhow!("Unexpected character: {c}")),
        }
    }
}

pub fn count_options(commands: Vec<Command>) -> u128 {
    let mut options: ShiftableSparseArray<u128> = ShiftableSparseArray::new();
    options.set(0, 1);

    for command in commands {
        match command {
            Command::Up => options.shift(1),
            Command::Down => options.shift(-1),
            Command::Unknown => {
                let mut new_options: ShiftableSparseArray<u128> = ShiftableSparseArray::new();

                for i in options.keys() {
                    new_options.incr(i + 1, options.get(i));
                    new_options.incr(i - 1, options.get(i));
                }

                options = new_options;
            }
        }

        options.set(-1, 0)
    }

    options.get(0)
}
