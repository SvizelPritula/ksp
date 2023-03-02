pub const GRAVITY: f64 = 9.81;

pub fn unit_arc_height(x: f64, middle: f64) -> f64 {
    1.0 - ((x - middle) / middle).powi(2)
}

pub fn throw_velocity(height: f64, middle: f64) -> Velocity {
    let g = GRAVITY;
    let sx = middle;
    let sy = height;

    let t = (2.0 * sy / g).sqrt();

    let vx = sx / t;
    let vy = g * t;

    Velocity::new(vx, vy)
}

#[derive(Debug, Clone, Copy)]
pub struct Velocity {
    pub x: f64,
    pub y: f64,
}

impl Velocity {
    pub fn new(x: f64, y: f64) -> Self {
        Velocity { x, y }
    }

    pub fn magnitude(&self) -> f64 {
        (self.x.powi(2) + self.y.powi(2)).sqrt()
    }

    pub fn angle(&self) -> f64 {
        self.y.atan2(self.x).to_degrees()
    }
}
