/*
 * Copyright (c) 2021. Davi Pereira dos Santos
 * This file is part of the hosh project.
 * Please respect the license - more about this in the section (*) below.
 *
 * hosh is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * hosh is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with hosh.  If not, see <http://www.gnu.org/licenses/>.
 *
 * (*) Removing authorship by any means, e.g. by distribution of derived
 * works or verbatim, obfuscated, compiled or rewritten versions of any
 * part of this work is a crime and is unethical regarding the effort and
 * time spent here.
 * Relevant employers or funding agencies will be notified accordingly.
 */

// #![feature(iterator_fold_self)]
use std::collections::VecDeque;
use std::str;
use std::time::Instant;

pub mod math;

use math::{digest, from_b62, int_to_perm, to_b62};
use crate::math::{PERM, DIGITS, NBYTES};

fn main() {
    for _i in 0..6 {
        let mut lst: VecDeque<(PERM, DIGITS)> = VecDeque::new();
        let now = Instant::now();
        for i in 1..10_000 {
            let content: [u8; NBYTES] = u128::to_be_bytes(876123876213876123873612 + i);
            let digest = digest(&content);
            let n = u128::from_be_bytes(digest);
            let perm = int_to_perm(&n);  // 350ns
            // let perm2 = &mut perm.clone();
            // let perm2 = mul(&perm, perm2);
            lst.push_front((perm, to_b62(&n)));
        }

        let t = now.elapsed().as_nanos() as f64 / 10_000.0;
        let res = to_b62(&295232799039604140847618609643519999999);
        let resd = from_b62(&res);
        let x: u128 = 340282366920938463463374607431768211455;
        let y: u128 = 2;
        println!(
            "{} {}us  <{}>  {} {}", math::add(&x, &math::ainv(&math::ainv(&y))),
            t.round() / 1000.0,
            str::from_utf8(&res).unwrap(),
            lst.len(),
            resd
        );
    }
}


// /// Take an array representing a sequence of 3-tuples and fold it through an arbitrary sandwich logic.
// fn keep_largest(lst: &[u8]) -> [u8; 3] {
//     lst.chunks(3).map(|x| [x[0], x[1], x[2]]).reduce(|x, y| [x[0], y[1], x[0]]).unwrap()
// }
// /*
// 3  |     lst.chunks(3).reduce(|x, y| [x[0], y[1], x[0]]).unwrap()
//    |                                 ^^^^^^^^^^^^^^^^^^
//    |                                 |
//    |                                 expected `&[u8]`, found array `[u8; 3]`
//    |                                 help: consider borrowing here: `&[x[0], y[1], x[0]]`
// */
//
// fn keep_largest2(lst: &[u8]) -> [u8; 3] {
//     let mut r: [u8; 3] = lst[..].try_into().unwrap();
//     for i in (3..lst.len()).step_by(3) {
//         let y = &lst[i..i + 3];
//         r = [r[0], y[1], r[0]];
//     }
//     r
// }
