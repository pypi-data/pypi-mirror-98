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

use blake3::{hash, Hasher};
use std::convert::TryInto;
use std::str;
#[rustversion::nightly]
use specialized_div_rem as sdr;
use std::ascii::escape_default;

const ALPH: [u8; 62] = *b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";
const ALPHREV: [usize; 123] = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0, 0, 10, 11, 12, 13, 14, 15, 16, 17,
    18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 0, 0, 0, 0, 0, 0, 36, 37, 38, 39, 40, 41,
    42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61,
];
pub const NBYTES: usize = 16;
pub const MAXN: u128 = 295232799039604140847618609643519999999;
pub const PERM_SIZE: usize = 34;
pub const NDIGITS: usize = 22;

pub type HEX = [u8; 2 * NBYTES];

pub type PERM = [u8; PERM_SIZE];
pub type DIGITS = [u8; NDIGITS];
/*
    NBYTES  > log2(34!)     = 127.7951206129691
    NDIGITS > log62(34!)    = 21.46303446361606
    MAXN                    = 34! - 1           = 6l6zBwhWj1aEJrTu8Ko2Rz
*/

pub fn b62_to_str(bytes: &[u8]) -> String {
    let mut visible = String::new();
    for &b in bytes {
        let part: Vec<u8> = escape_default(b).collect();
        visible.push_str(str::from_utf8(&part).unwrap());
    }
    visible
}

pub fn digest(bytes: &[u8]) -> [u8; NBYTES] {
    let mut h: [u8; 16] = if bytes.len() < 130000 {
        hash(bytes).as_bytes()[NBYTES..2 * NBYTES].try_into().unwrap()
    } else {
        let mut hasher = Hasher::new();
        hasher.update_with_join::<blake3::join::RayonJoin>(bytes);
        hasher.finalize().as_bytes()[NBYTES..2 * NBYTES].try_into().unwrap()
    };
    h[0] = h[0] & 127; //h[0] %= 128;
    h
}

#[rustversion::nightly]
#[inline]
fn inplace_divmod(a: &mut u128, b: u128) -> u128 {
    let qr = sdr::u128_div_rem_delegate(*a, b);
    *a = qr.0;
    qr.1
}

#[rustversion::stable]
#[inline]
fn inplace_divmod(a: &mut u128, b: u128) -> u128 {
    let r = *a % b;
    *a /= b;
    r
}

#[inline]
pub fn to_b62(n: &u128) -> DIGITS {
    let mut s = [0 as u8; NDIGITS];
    let base: u128 = 62;
    let mut quot = *n;
    for i in (0..NDIGITS).rev() {
        let rem = inplace_divmod(&mut quot, base);
        s[i] = ALPH[rem as usize];
    }
    s
}

pub fn from_b62(digits: &[u8]) -> u128 {
    let mut power: u128 = 1;
    let mut iter = digits.iter().rev();
    let fst = *iter.next().unwrap() as usize;
    let mut n: u128 = ALPHREV[fst] as u128;
    for idx in iter {
        let c = ALPHREV[*idx as usize] as u128;
        power *= 62;
        n += power * c;
    }
    n
}

#[inline]
pub fn int_to_perm(n: &u128) -> PERM {
    if n > &295232799039604140847618609643519999999u128 {
        panic!(
            "One operand exceeeds the order 34! of the set of all 34-permutations.
            Maximum value: 295232799039604140847618609643519999999
            Hint: operand %= 34!
            Alternative 2: Set at least the most significant bit to zero.
            Alternative 3: Set at least the most significant byte to zero.
            Alternative 4: Set at least the most significant base-62 digit to zero."
        )
    }
    let mut avail: Vec<u8> = (0..PERM_SIZE as u8).collect();
    let mut quot = *n;
    let mut perm: [u8; PERM_SIZE] = [0; PERM_SIZE];
    for i in (1..=PERM_SIZE).rev() {
        // let rem = inplace_divmod(&mut quot, base);
        let rem = quot % (i as u128);
        quot = quot / (i as u128);
        perm[PERM_SIZE - i] = avail.remove(rem as usize);
    }
    perm
}

pub fn perm_to_int(p: &[u8]) -> u128 {
    let mut avail: Vec<u8> = (0..PERM_SIZE as u8).collect();
    let mut i: u128 = 1;
    let mut n: u128 = 0;
    for radix in (1..=PERM_SIZE).rev() {
        let idx = avail.iter().position(|&x| x == p[PERM_SIZE - radix]).unwrap();
        avail.remove(idx);
        n += (idx as u128) * i;
        i *= radix as u128;
    }
    n
}

#[inline]
pub fn add(a: &u128, b: &u128) -> u128 {
    a.wrapping_add(*b)
}

#[inline]
pub fn ainv(a: &u128) -> u128 {
    u128::max_value().wrapping_sub(*a).wrapping_add(1)
}

#[inline]
pub fn mul(a: &[u8], b: &[u8]) -> PERM {
    let mut r = [0 as u8; PERM_SIZE];
    for i in 0..PERM_SIZE {
        r[i] = a[b[i as usize] as usize]
    }
    r
}


#[inline]
pub fn minv(a: &[u8]) -> [u8; PERM_SIZE] {
    let mut r = [0 as u8; PERM_SIZE];
    for i in 0..PERM_SIZE {
        r[a[i] as usize] = i as u8
    }
    r
}


// #[inline]
// pub fn transpose(a: &[u8]) -> PERM {  //funciona? faz sentido?
//     let mut tr_ls = [0 as u8; PERM_SIZE];
//     let last = PERM_SIZE - 1;
//     for i in 0..PERM_SIZE {
//         tr_ls[last - a[a[i] as usize] as usize] = last as u8 - a[i];
//     }
//     return tr_ls;
// }


// pub fn fnwrap<'a>(f: fn(&mut [u8], &mut [u8])) -> impl Fn(&mut [u8], &'a mut [u8]) ->
// &'a mut [u8] {
//     move |a, b| {
//         f(a, b);
//         b
//     }
// }


// pub fn mul(a: &[u8], b: &mut [u8]) {
//     // let mut r = [0 as u8; PERM_SIZE];
//     for i in 0..PERM_SIZE {
//         b[i] = a[b[i as usize] as usize]
//     }
// }
