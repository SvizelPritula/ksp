use std::{env::args, process::ExitCode};

use fibonacci::fibonacci;
use num::BigInt;

fn main() -> ExitCode {
    let Some(n) = args().nth(1) else {
        let name = args().nth(0).unwrap_or_else(|| String::from("fibonacci"));

        eprintln!("Usage: {name} [n]");
        return ExitCode::FAILURE;
    };

    let n = match n.parse() {
        Ok(n) => n,
        Err(err) => {
            eprintln!("{err}");
            return ExitCode::FAILURE;
        }
    };

    let result: BigInt = fibonacci(n);

    println!("{result}");
    ExitCode::SUCCESS
}
