use std::{collections::HashMap, ops::Add};

#[derive(Default)]
pub struct ShiftableSparseArray<T>
where
    T: Default + Copy + Eq,
{
    map: HashMap<isize, T>,
    offset: isize,
}

impl<T: Default + Copy + Eq> ShiftableSparseArray<T> {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn shift(&mut self, offset: isize) {
        self.offset -= offset;
    }

    pub fn get(&self, index: isize) -> T {
        match self.map.get(&(index + self.offset)) {
            Some(value) => *value,
            None => T::default(),
        }
    }

    pub fn set(&mut self, index: isize, value: T) {
        if value != T::default() {
            self.map.insert(index + self.offset, value);
        } else {
            self.map.remove(&(index + self.offset));
        }
    }

    pub fn keys(&self) -> impl Iterator<Item = isize> + '_ {
        self.map.keys().map(|i| i - self.offset)
    }
}

impl<T: Default + Copy + Eq + Add<Output = T>> ShiftableSparseArray<T> {
    pub fn incr(&mut self, index: isize, value: T) {
        self.set(index, self.get(index) + value);
    }
}
