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

#[macro_use]
extern crate arrayref;

use std::convert::TryInto;

use pyo3::{PyClass, PyNativeType, PyObjectProtocol, PyTypeInfo, wrap_pyfunction};
use pyo3::prelude::*;
use pyo3::types::{PyString, PyBytes, PyList, PyInt, PyTuple};

use math::{digest, DIGITS, HEX, int_to_perm, PERM, PERM_SIZE, perm_to_int, to_b62};

pub mod math;

#[inline]
fn pybytes(bin: &[u8]) -> PyObject {
    let gil = Python::acquire_gil();
    PyBytes::new(gil.python(), bin).into()
}


/// A Python module implemented in Rust.
#[pymodule]
#[cfg(not(test))]
fn hosh(py: Python, m: &PyModule) -> PyResult<()> {
    let _ = py;
    m.add_function(wrap_pyfunction!(b62, m)?)?;
    m.add_function(wrap_pyfunction!(mul, m)?)?;
    m.add_function(wrap_pyfunction!(div, m)?)?;
    m.add_function(wrap_pyfunction!(minv, m)?)?;
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(ainv, m)?)?;
    m.add_function(wrap_pyfunction!(muls, m)?)?;
    m.add_function(wrap_pyfunction!(mulpairs, m)?)?;
    m.add_function(wrap_pyfunction!(n_bin_id_fromblob, m)?)?;
    m.add_function(wrap_pyfunction!(n_bin_fromid, m)?)?;
    m.add_function(wrap_pyfunction!(n_id_fromperm, m)?)?;
    m.add_function(wrap_pyfunction!(bin_id_fromn, m)?)?;
    Ok(())
}

/// doc
#[pyfunction]
fn b62(blob: &[u8]) -> PyResult<String> {
    let ret = math::b62_to_str(&math::to_b62(&u128::from_be_bytes(math::digest(blob))));
    Ok(ret.to_string())
}

/// doc
#[pyfunction]
fn muls(perms: Vec<&PyBytes>) -> PyObject {
    let mut r: PERM = perms[0].as_bytes().try_into().unwrap();
    for a in &perms[1..] {
        r = math::mul(&r, a.as_bytes());
    }
    pybytes(&r)
}

#[pyfunction]
fn mulpairs(perms: Vec<&PyBytes>) -> PyObject {
    let mut v = Vec::<&PyBytes>::new();
    let gil = Python::acquire_gil();
    let py = gil.python();
    for chunk in perms.chunks(2) {
        let a: PERM = chunk[0].as_bytes().try_into().unwrap();
        let b = chunk[1].as_bytes();
        let bin = math::mul(&a, b);
        v.push(&PyBytes::new(py, &bin));
    }
    v.into_py(py)
}

#[pyfunction]
fn n_bin_id_fromblob(blob: &[u8]) -> (PyObject, PyObject, String) {
    let n = u128::from_be_bytes(digest(blob));
    let bin = int_to_perm(&n);
    let id = to_b62(&n);
    let gil = Python::acquire_gil();
    let idstr = unsafe { String::from_utf8_unchecked(id.to_vec()) };
    (n.to_object(gil.python()), PyBytes::new(gil.python(), &bin).into(), idstr)
}

#[pyfunction]
fn n_id_fromperm(a: &[u8]) -> (PyObject, String) {
    let n = perm_to_int(&a);
    let id = to_b62(&n);
    let gil = Python::acquire_gil();
    let idstr = unsafe { String::from_utf8_unchecked(id.to_vec()) };
    (n.to_object(gil.python()), idstr)
}

#[pyfunction]
fn bin_id_fromn(n: u128) -> (PyObject, String) {
    let bin = int_to_perm(&n);
    let id = to_b62(&n);
    let gil = Python::acquire_gil();
    let idstr = unsafe { String::from_utf8_unchecked(id.to_vec()) };
    (PyBytes::new(gil.python(), &bin).into(), idstr)
}

#[pyfunction]
fn n_bin_fromid(id: String) -> (PyObject, PyObject) {
    let n = math::from_b62(id.as_bytes());
    let bin = int_to_perm(&n);
    let gil = Python::acquire_gil();
    (n.to_object(gil.python()), PyBytes::new(gil.python(), &bin).into())
}

/// doc
#[pyfunction]
fn mul(a: &[u8], b: &[u8]) -> PyObject {
    let r = math::mul(&a, &b);
    pybytes(&r)
}

/// doc
#[pyfunction]
fn div(a: &[u8], b: &[u8]) -> PyObject {
    let r = math::mul(&a, &math::minv(&b));
    pybytes(&r)
}

/// doc
#[pyfunction]
fn minv(a: &[u8]) -> PyObject {
    let r = math::minv(&a);
    pybytes(&r)
}

/// doc
#[pyfunction]
fn add(a: u128, b: u128) -> u128 {
    math::add(&a, &b)
}

/// doc
#[pyfunction]
fn ainv(a: u128) -> u128 {
    math::ainv(&a)
}


/*
#[pyfunction]
fn mulmany_par0(perms: Vec<(&PyBytes, &PyBytes)>) -> PyObject {
    let mut v = Vec::<&PyBytes>::new();
    let gil = Python::acquire_gil();
    let py = gil.python();
    for (a, b) in perms {
        let bin = math::mul(a.as_bytes(), b.as_bytes());
        v.push(&PyBytes::new(py, &bin));
    }
    v.into_py(py)
}
*/

/*
Rust class abandoned, reason:
    attribute access is too slow when compared to using a class written in python.

/// A Python class implemented in Rust.
#[cfg(not(test))]
#[pyclass(module = "hash", subclass, freelist = 10)]
struct Hash {
    n: u128,
    id: DIGITS,
    bin: PERM,
}

#[pymethods]
#[cfg(not(test))]
impl Hash {
    #[new]
    #[args(perm = "&[255; PERM_SIZE]", blob = "&[255; 1]")]
    fn new(perm: &[u8], blob: &[u8]) -> Self {
        let tup = if perm[0] != 255 {
            let n = perm_to_int(perm);
            let bin = perm[..PERM_SIZE].try_into().unwrap();
            (n, bin)
        } else if blob.len() > 1 {
            let n = digest_to_int(&digest(blob));
            let bin = int_to_perm(&n);
            (n, bin)
        } else {
            panic!("Exactly one argument is required: perm, blob.")
        };
        let (n, bin) = tup;
        let id = to_b62(&n);
        Hash { n, id, bin }
    }

    #[getter]
    fn hex(&self) -> PyResult<String> {
        Ok(format!("{:x}", self.n))
    }

    #[getter]
    fn n(&self) -> PyResult<u128> {
        Ok(self.n)
    }

    #[getter]
    fn id(&self) -> PyObject {
        pystr(&self.id)
    }

    #[getter]
    fn bin(&self) -> PyObject {
        pystr(&self.bin)
    }
}

#[cfg(not(test))]
unsafe impl Send for Hash {}

#[pyproto]
#[cfg(not(test))]
impl PyObjectProtocol for Hash {
    fn __str__(&self) -> PyObject {
        pystr(&self.id)
    }
}

 */
