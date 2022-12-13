use std::{cmp::Reverse, collections::BinaryHeap};

use anyhow::{Error, Result};

pub struct Dependency {
    pub dependant: usize,
    pub dependency: usize,
}

#[derive(Clone)]
struct Potion {
    id: usize,
    preparation_time: u64,
    dependencies: usize,
    dependents: Vec<usize>,
    start_time: Option<u64>,
}

pub fn get_start_times(
    preparation_times: Vec<u64>,
    dependencies: Vec<Dependency>,
) -> Result<Vec<u64>> {
    let mut potions: Vec<Potion> = preparation_times
        .iter()
        .enumerate()
        .map(|(id, preparation_time)| Potion {
            id,
            preparation_time: *preparation_time,
            dependents: vec![],
            dependencies: 0,
            start_time: None,
        })
        .collect();

    for Dependency {
        dependant,
        dependency,
    } in dependencies
    {
        potions[dependant].dependencies += 1;
        potions[dependency].dependents.push(dependant);
    }

    let mut ready: Vec<usize> = potions
        .iter()
        .filter(|p| p.dependencies == 0)
        .map(|p| p.id)
        .collect();

    let mut time: u64 = 0;

    let mut queue: BinaryHeap<(Reverse<u64>, usize)> = BinaryHeap::new();

    loop {
        while let Some(id) = ready.pop() {
            potions[id].start_time = Some(time);
            queue.push((Reverse(time + potions[id].preparation_time), id));
        }

        if let Some((Reverse(new_time), id)) = queue.pop() {
            time = new_time;

            for dependant_id in potions[id].dependents.clone() {
                potions[dependant_id].dependencies -= 1;

                if potions[dependant_id].dependencies == 0 {
                    ready.push(dependant_id);
                }
            }
        } else {
            break;
        }
    }

    potions
        .iter()
        .map(|p| p.start_time.ok_or(Error::msg("Dependency cycle detected")))
        .collect()
}

impl Ord for Potion {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        let ord = self.dependencies.cmp(&other.dependencies);

        if ord.is_ne() {
            ord
        } else {
            self.id.cmp(&other.id)
        }
    }
}
impl Eq for Potion {}
impl PartialEq for Potion {
    fn eq(&self, other: &Self) -> bool {
        self.cmp(other).is_eq()
    }

    fn ne(&self, other: &Self) -> bool {
        self.cmp(other).is_ne()
    }
}
impl PartialOrd for Potion {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
