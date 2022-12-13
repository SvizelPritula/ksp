use std::{
    fmt::Debug,
    ops::{Add, Div, Index, IndexMut, Mul, Sub},
};

use num::{One, Zero};

#[derive(Default, Clone, Hash, PartialEq, Eq)]
pub struct Vector<T> {
    vec: Vec<T>,
}

impl<T> Vector<T> {
    pub fn new(vec: Vec<T>) -> Self {
        Vector { vec }
    }

    pub fn len(&self) -> usize {
        self.vec.len()
    }

    pub fn iter(&self) -> std::slice::Iter<T> {
        self.vec.iter()
    }
}

impl<T> Vector<T>
where
    T: Zero,
{
    pub fn zeroes(size: usize) -> Self {
        let mut vec = Vec::with_capacity(size);

        for _ in 0..size {
            vec.push(T::zero());
        }

        Vector::new(vec)
    }

    pub fn axis(direction: usize, magnitude: T, size: usize) -> Self {
        let mut value = Vector::zeroes(size);
        value[direction] = magnitude;
        value
    }
}

impl<T> Vector<T>
where
    T: Zero + One,
{
    pub fn unit(direction: usize, size: usize) -> Self {
        Vector::axis(direction, T::one(), size)
    }
}

impl<T> From<Vec<T>> for Vector<T> {
    fn from(vec: Vec<T>) -> Self {
        Vector { vec }
    }
}

impl<T> From<Vector<T>> for Vec<T> {
    fn from(vector: Vector<T>) -> Self {
        vector.vec
    }
}

impl<T> IntoIterator for Vector<T> {
    type Item = T;

    type IntoIter = <Vec<T> as IntoIterator>::IntoIter;

    fn into_iter(self) -> Self::IntoIter {
        self.vec.into_iter()
    }
}

impl<T> FromIterator<T> for Vector<T> {
    fn from_iter<I: IntoIterator<Item = T>>(iter: I) -> Self {
        Vec::from_iter(iter).into()
    }
}

impl<T: Debug> Debug for Vector<T> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        self.vec.fmt(f)
    }
}

impl<'a, 'b, T, U> Add<&'b Vector<U>> for &'a Vector<T>
where
    T: Add<U> + Clone,
    U: Clone,
{
    type Output = Vector<<T as Add<U>>::Output>;

    fn add(self, rhs: &Vector<U>) -> Self::Output {
        if self.vec.len() != rhs.vec.len() {
            panic!("mismatched vector length")
        }

        self.vec
            .iter()
            .zip(rhs.vec.iter())
            .map(|(a, b)| a.clone() + b.clone())
            .collect()
    }
}

impl<'a, 'b, T, U> Sub<&'b Vector<U>> for &'a Vector<T>
where
    T: Sub<U> + Clone,
    U: Clone,
{
    type Output = Vector<<T as Sub<U>>::Output>;

    fn sub(self, rhs: &Vector<U>) -> Self::Output {
        if self.vec.len() != rhs.vec.len() {
            panic!("mismatched vector length")
        }

        self.vec
            .iter()
            .zip(rhs.vec.iter())
            .map(|(a, b)| a.clone() - b.clone())
            .collect()
    }
}

impl<'a, T, U> Mul<U> for &'a Vector<T>
where
    T: Mul<U> + Clone,
    U: Clone,
{
    type Output = Vector<<T as Mul<U>>::Output>;

    fn mul(self, rhs: U) -> Self::Output {
        self.vec.iter().map(|a| a.clone() * rhs.clone()).collect()
    }
}

impl<'a, T, U> Div<U> for &'a Vector<T>
where
    T: Div<U> + Clone,
    U: Clone,
{
    type Output = Vector<<T as Div<U>>::Output>;

    fn div(self, rhs: U) -> Self::Output {
        self.vec.iter().map(|a| a.clone() / rhs.clone()).collect()
    }
}

impl<T, I> Index<I> for Vector<T>
where
    Vec<T>: Index<I>,
{
    type Output = <Vec<T> as Index<I>>::Output;

    fn index(&self, index: I) -> &Self::Output {
        &self.vec[index]
    }
}

impl<T, I> IndexMut<I> for Vector<T>
where
    Vec<T>: IndexMut<I>,
{
    fn index_mut(&mut self, index: I) -> &mut Self::Output {
        &mut self.vec[index]
    }
}
