use crate::{physics::unit_arc_height, range::Range};

#[derive(Debug, Clone, Copy)]
pub struct Obstacle {
    bottom: f64,
    top: f64,
    left: f64,
    right: f64,
}

impl Obstacle {
    pub fn new(x1: f64, y1: f64, x2: f64, y2: f64) -> Self {
        Obstacle {
            bottom: y1.min(y2),
            top: y1.max(y2),
            left: x1.min(x2),
            right: x1.max(x2),
        }
    }

    pub fn blocked_height_range(&self, middle: f64) -> Range {
        let left_bottom = self.bottom / unit_arc_height(self.left, middle);
        let right_bottom = self.bottom / unit_arc_height(self.right, middle);

        let left_top = self.top / unit_arc_height(self.left, middle);
        let right_top = self.top / unit_arc_height(self.right, middle);

        let mut bottom = left_bottom.min(right_bottom);
        let mut top = left_top.max(right_top);

        if (self.left..self.right).contains(&middle) {
            bottom = bottom.min(self.bottom);
            top = top.max(self.top);
        }

        Range::new(bottom, top)
    }
}
