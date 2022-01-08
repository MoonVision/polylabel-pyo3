use geo::Polygon;
use polylabel::errors::PolylabelError as PolylabelErrorRS;
use polylabel::polylabel;
use pyo3::create_exception;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use std::fmt;
use std::fmt::{Debug, Display, Formatter};

create_exception!(polylabel_pyo3, PolylabelError, PyValueError);

#[derive(Debug)]
struct Error(PolylabelErrorRS);

impl std::error::Error for Error {}

impl From<PolylabelErrorRS> for Error {
    fn from(e: PolylabelErrorRS) -> Self {
        Error(e)
    }
}

impl From<Error> for PyErr {
    fn from(e: Error) -> Self {
        PolylabelError::new_err(format!("{}", e))
    }
}

impl Display for Error {
    fn fmt(&self, f: &mut Formatter<'_>) -> fmt::Result {
        Display::fmt(&self.0, f)
    }
}

/// Calculate visual center from exterior points
#[pyfunction]
fn polylabel_ext(exterior: Vec<(f64, f64)>, tolerance: f64) -> Result<(f64, f64), Error> {
    let poly = Polygon::new(exterior.into(), vec![]);
    let point = polylabel(&poly, &tolerance)?;
    Ok(point.x_y())
}

/// Polylabel algorithm in Rust.
#[pymodule]
fn polylabel_pyo3(py: Python, m: &PyModule) -> PyResult<()> {
    m.add("PolylabelError", py.get_type::<PolylabelError>())?;
    m.add_function(wrap_pyfunction!(polylabel_ext, m)?)?;
    Ok(())
}
