use crate::{
    obstacle::Obstacle,
    physics::{throw_velocity, Velocity},
    range::Range,
};

pub fn solve(obstacles: Vec<Obstacle>, target: f64) -> Option<Velocity> {
    let middle = target / 2.0;

    let blocked = obstacles
        .iter()
        .map(|o| o.blocked_height_range(middle))
        .collect();

    let blocked = Range::union(blocked);

    let optimal_height = middle / 2.0;
    let optimal_height = if blocked.iter().any(|r| r.contains(optimal_height)) {
        None
    } else {
        Some(optimal_height)
    };

    let candidate_heights = blocked
        .iter()
        .flat_map(|r| [r.bottom, r.top])
        .chain(optimal_height);

    candidate_heights
        .map(|height| throw_velocity(height, middle))
        .min_by(|a, b| a.magnitude().total_cmp(&b.magnitude()))
}
