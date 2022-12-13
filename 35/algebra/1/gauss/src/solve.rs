use num::{BigRational, Zero};

use crate::{
    eliminate::{count_zeros, eliminate},
    vector::Vector,
};

pub enum Solution {
    None,
    Single(Vector<BigRational>),
    Multiple(Vec<Vector<BigRational>>),
}

fn evaluate(
    values: &[Vector<BigRational>],
    factors: &[BigRational],
    size: usize,
) -> Vector<BigRational> {
    values
        .iter()
        .zip(factors.iter())
        .map(|(a, b)| a * b)
        .fold(Vector::zeroes(size), |a, b| &a + &b)
}

fn solve_impl(equations: Vec<Vector<BigRational>>) -> Option<Vec<Vector<BigRational>>> {
    let equations: Vec<Vector<BigRational>> = eliminate(equations);

    let mut solution: Vec<Vector<BigRational>> = vec![Vector::default(); equations.len()];
    let mut first_known_solution = equations.len();

    for equation in equations.iter().rev() {
        let column = count_zeros(&equation);

        if column > equations.len() {
            continue;
        }
        if column == equations.len() {
            return None;
        }

        for column in 0..first_known_solution {
            solution[column] = Vector::unit(column, equations.len() + 1);
        }

        let rhs = &equation[equations.len()];
        let known = &equation[(column + 1)..equations.len()];
        let unknown = &equation[column];

        let known = evaluate(
            &solution[(column + 1)..equations.len()],
            &known,
            equations.len() + 1,
        );

        let rhs = Vector::axis(equations.len(), rhs.clone(), equations.len() + 1);

        let value = &(&rhs - &known) / unknown;

        if column < first_known_solution {
            solution[column] = value;
            first_known_solution = column;
        } else {
            if value != solution[column] {
                return None;
            }
        }
    }

    for column in 0..first_known_solution {
        solution[column] = Vector::unit(column, equations.len() + 1);
    }

    Some(solution)
}

pub fn solve(equations: Vec<Vector<BigRational>>) -> Solution {
    match solve_impl(equations) {
        Some(values) => {
            if values
                .iter()
                .all(|v| v[..v.len() - 1].iter().all(|e| e.is_zero()))
            {
                Solution::Single(
                    values
                        .into_iter()
                        .map(|v| v.into_iter().last().unwrap())
                        .collect(),
                )
            } else {
                Solution::Multiple(values)
            }
        }
        None => Solution::None,
    }
}
