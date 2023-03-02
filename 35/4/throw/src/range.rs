#[derive(Debug, Clone, Copy)]
pub struct Range {
    pub bottom: f64,
    pub top: f64,
}

impl Range {
    pub fn new(bottom: f64, top: f64) -> Self {
        Range { bottom, top }
    }

    pub fn contains(&self, value: f64) -> bool {
        self.bottom <= value && value <= self.top
    }

    pub fn union(mut ranges: Vec<Range>) -> Vec<Range> {
        ranges.sort_unstable_by(|a, b| a.bottom.total_cmp(&b.bottom));
        let mut result = Vec::new();

        let mut active_range: Option<Range> = None;

        for range in ranges {
            if let Some(active_range) = &mut active_range {
                if active_range.contains(range.bottom) {
                    active_range.top = active_range.top.max(range.top);
                } else {
                    result.push(*active_range);
                    *active_range = range;
                }
            } else {
                active_range = Some(range);
            }
        }

        if let Some(range) = active_range {
            result.push(range)
        }

        result
    }
}
