use num::{BigRational, Zero};

use crate::vector::Vector;

pub fn count_zeros(vector: &Vector<BigRational>) -> usize {
    vector
        .iter()
        .enumerate()
        .take_while(|(_, v)| v.is_zero())
        .count()
}

fn remove_least_zeros(equations: &mut Vec<Vector<BigRational>>) -> Option<Vector<BigRational>> {
    let (index, _) = equations
        .iter()
        .enumerate()
        .min_by_key(|(_, v)| count_zeros(v))?;
    Some(equations.remove(index))
}

pub fn eliminate(mut equations: Vec<Vector<BigRational>>) -> Vec<Vector<BigRational>> {
    let mut processed = Vec::with_capacity(equations.len());

    while let Some(base) = remove_least_zeros(&mut equations) {
        let column = count_zeros(&base);

        if column < base.len() {
            for equation in &mut equations {
                *equation = &(&*equation * &base[column]) - &(&base * &equation[column]);
            }
        }

        processed.push(base);
    }

    processed
}
