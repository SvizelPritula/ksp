use anyhow::Result;
use solve::{count_options, Command};
use text_io::try_read;

mod solve;
mod sparse;

fn main() -> Result<()> {
    let _: usize = try_read!()?;

    let commands: String = try_read!("{}\n")?;
    let commands: Vec<Command> = commands
        .chars()
        .map(Command::try_from)
        .collect::<Result<Vec<Command>>>()?;

    let options = count_options(commands);

    println!("{options}");

    Ok(())
}
