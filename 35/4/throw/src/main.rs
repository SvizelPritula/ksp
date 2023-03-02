use std::io::stdin;

use anyhow::Result;
use obstacle::Obstacle;
use solve::solve;
use token_read::TokenReader;

mod obstacle;
mod physics;
mod range;
mod solve;

fn main() -> Result<()> {
    let mut input = TokenReader::new(stdin().lock());

    let (task_count,): (usize,) = input.line()?;

    for _ in 0..task_count {
        let (obstacle_count, target): (usize, f64) = input.line()?;
        let mut obstacles = Vec::with_capacity(obstacle_count);

        for line in input.take(obstacle_count) {
            let (x1, y1, x2, y2) = line?;
            obstacles.push(Obstacle::new(x1, y1, x2, y2));
        }

        if let Some(velocity) = solve(obstacles, target) {
            println!(
                "{angle} {magnitude}",
                angle = velocity.angle(),
                magnitude = velocity.magnitude()
            );
        } else {
            println!("no solution");
        }
    }

    Ok(())
}
