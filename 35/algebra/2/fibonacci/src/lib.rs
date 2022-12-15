use nalgebra::{matrix, vector, ClosedAdd, ClosedMul, Scalar};
use num::{One, Zero};

pub fn fibonacci<T>(n: u32) -> T
where
    T: Scalar + ClosedAdd + ClosedMul + Zero + One,
{
    let mat = matrix![T::zero(), T::one(); T::one(), T::one()];
    let vec = vector![T::zero(), T::one()];

    let result = mat.pow(n) * vec;

    result.x.clone()
}
