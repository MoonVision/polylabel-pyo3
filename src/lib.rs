use geo::{Coordinate, LineString, Polygon};
use numpy::ndarray::Axis;
use numpy::PyReadonlyArray2;
use polylabel::errors::PolylabelError as PolylabelErrorRS;
use polylabel::polylabel;
use pyo3::create_exception;
use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;

use std::fmt;
use std::fmt::{Debug, Display, Formatter};

create_exception!(polylabel_pyo3, PolylabelError, PyValueError);
create_exception!(polylabel_pyo3, PolylabelShapeError, PyTypeError);

#[derive(Debug)]
enum Error {
    Poly(PolylabelErrorRS),
    Py(PyErr),
}

impl std::error::Error for Error {}

impl From<PolylabelErrorRS> for Error {
    fn from(e: PolylabelErrorRS) -> Self {
        Error::Poly(e)
    }
}

impl From<Error> for PyErr {
    fn from(err: Error) -> Self {
        match err {
            Error::Py(e) => e,
            Error::Poly(_) => PolylabelError::new_err(format!("{}", err)),
        }
    }
}

impl From<PyErr> for Error {
    fn from(e: PyErr) -> Self {
        Self::Py(e)
    }
}

impl Display for Error {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        Display::fmt(&self, f)
    }
}

// todo: f32, generic python Iterable[Iterable[float]]

/// Calculate visual center from pairs of exterior points
#[pyfunction]
fn polylabel_ext(exterior: Vec<(f64, f64)>, tolerance: f64) -> Result<(f64, f64), Error> {
    let poly = Polygon::new(exterior.into(), vec![]);
    let point = polylabel(&poly, &tolerance)?;
    Ok(point.x_y())
}

/// Calculate visual center from a two dimensional array
#[pyfunction]
fn polylabel_ext_np(exterior: PyReadonlyArray2<f64>, tolerance: f64) -> Result<(f64, f64), Error> {
    // we have to clone anyway, because LineString owns a Vec<Coordinate> and
    // - Polygon may push one Coordinate to close it on ::new
    // - Coordinate has no C/defined memory layout
    let dim1 = exterior.shape()[1];
    if dim1 != 2 {
        return Err(PolylabelShapeError::new_err(format!(
            "Expected axis(1) of shape 2, got {}",
            dim1
        ))
        .into());
    }
    let mut coords: Vec<Coordinate<f64>> = Vec::with_capacity(exterior.len() + 1);
    coords.extend(exterior.as_array().axis_iter(Axis(0)).map(|c| Coordinate { x: c[0], y: c[1] }));
    let line = LineString(coords);
    let poly = Polygon::new(line, vec![]);
    let point = polylabel(&poly, &tolerance)?;
    Ok(point.x_y())
}

/// Polylabel algorithm in Rust.
#[pymodule]
fn polylabel_pyo3(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("PolylabelError", py.get_type::<PolylabelError>())?;
    m.add("PolylabelShapeError", py.get_type::<PolylabelShapeError>())?;
    m.add_function(wrap_pyfunction!(polylabel_ext, m)?)?;
    m.add_function(wrap_pyfunction!(polylabel_ext_np, m)?)?;
    Ok(())
}
