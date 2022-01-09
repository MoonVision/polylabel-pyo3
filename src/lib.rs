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

fn try_from_coords(coord: &PyAny) -> PyResult<Coordinate<f64>> {
    Ok(Coordinate {
        x: PyAny::extract::<f64>(coord.get_item(0)?)?,
        y: PyAny::extract::<f64>(coord.get_item(1)?)?,
    })
}

/// Calculate pole of accessibility from pairs of exterior points.
///
/// Args:
///   exterior: iterable of elements which are accessed at 0 and 1 for coordinates
///   tolerance: stop sub-dividing a cell if the distance gained between exterior and
///     its centroid was less than this value
///
/// Returns:
///   coordinates as Tuple[float, float], (0,0) if exterior is degenerate
////
/// Raises:
///     TypeError: If exterior is not iterable
///     IndexError: If an element can't be indexed at 0 and 1
///     PolylabelError: Calculation error during grid-based search
#[pyfunction]
#[pyo3(text_signature = "(exterior, tolerance)")]
fn polylabel_ext(exterior: &PyAny, tolerance: f64) -> Result<(f64, f64), Error> {
    let coord_iter = exterior.iter()?.map(|c| c.and_then(try_from_coords));
    let coords = coord_iter.collect::<Result<Vec<_>, _>>()?;
    let poly = Polygon::new(LineString(coords), vec![]);
    let point = polylabel(&poly, &tolerance)?;
    Ok(point.x_y())
}

/// Calculate pole of accessibility from a two dimensional floating point array.
///
/// Args:
///   exterior (Nx2): array of coordinates
///   tolerance: stop sub-dividing a cell if the distance gained between exterior and
///     its centroid was less than this value
///
/// Returns:
///   coordinates as Tuple[float, float], (0,0) if exterior is degenerate
////
/// Raises:
///     TypeError: If exterior has wrong dtype (only np.float64 supported) or rank
///     PolylabelShapeError: If axis 1 is not of length 2
///     PolylabelError: Calculation error during grid-based search
#[pyfunction]
#[pyo3(text_signature = "(exterior, tolerance)")]
fn polylabel_ext_np(exterior: PyReadonlyArray2<f64>, tolerance: f64) -> Result<(f64, f64), Error> {
    // todo: f32
    // we have to clone anyway, because LineString owns a Vec<Coordinate> and
    // - Polygon may push one Coordinate to close it on ::new
    // - Coordinate has no C/defined memory layout
    let dim1 = exterior.shape()[1];
    if dim1 != 2 {
        return Err(PolylabelShapeError::new_err(format!(
            "Expected axis(1) of length 2, got {}",
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
