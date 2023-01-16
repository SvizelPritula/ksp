use std::{collections::BTreeMap, mem::swap};

#[derive(Debug, Clone, Copy)]
pub struct Lid {
    pub start: usize,
    pub end: usize,
    pub id: usize,
}

impl Lid {
    pub fn contains(&self, position: usize) -> bool {
        self.start <= position && position <= self.end
    }
}

pub fn solve(cases: &Vec<u64>, mut lids: Vec<Lid>) -> BTreeMap<usize, usize> {
    lids.sort_by_key(|lid| (lid.end, lid.start));

    let mut placements: Vec<(Lid, usize)> = Vec::new();

    for lid in lids {
        let mut start = lid.start;

        for (lid, pos) in placements.iter().rev() {
            if *pos >= start {
                start = lid.start;
            }
        }

        let start = start;
        let end = lid.end;

        let mut placement = None;

        for position in start..=end {
            if placements.binary_search_by_key(&position, |p| p.1).is_err() {
                let is_better = match placement {
                    Some(placement) => cases[position] > cases[placement],
                    None => true,
                };

                if is_better {
                    placement = Some(position);
                }
            }
        }

        if let Some(mut placement) = placement {
            for (lid, position) in placements.iter_mut() {
                if lid.contains(placement) && placement < *position {
                    swap(position, &mut placement);
                }
            }

            placements.push((lid, placement));
        }
    }

    placements.iter().map(|(lid, pos)| (lid.id, *pos)).collect()
}
