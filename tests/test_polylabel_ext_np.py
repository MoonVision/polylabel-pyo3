import numpy as np
import pytest
from polylabel_pyo3 import PolylabelShapeError, polylabel_ext_np

from .fixtures import polys_degenerate, polys_ok

polys_ok_np = {
    name: (np.array(a, dtype=np.float64), t, e) for name, (a, t, e) in polys_ok.items()
}
polys_degenerate_np = [np.array(a, dtype=np.float64) for a in polys_degenerate]


def test_empty():
    assert polylabel_ext_np(np.zeros((0, 2)), 0.1) == (0.0, 0.0)


def test_wrong_type():
    with pytest.raises(TypeError):
        polylabel_ext_np([(0.0, 1.0), (1.0, 2.0)], 1.0)


def test_wrong_shape_and_type():
    with pytest.raises(TypeError):
        polylabel_ext_np(None, 2.0)


def test_wrong_np_shape_dim3():
    with pytest.raises(TypeError):
        polylabel_ext_np(np.zeros((2, 3, 4)), 1.0)


def test_wrong_np_shape_dim2():
    with pytest.raises(PolylabelShapeError):
        polylabel_ext_np(np.zeros((2, 3)), 1.0)


def test_wrong_np_dtype():
    with pytest.raises(TypeError):
        polylabel_ext_np(np.zeros((2, 4), dtype=np.float32), 1.0)


@pytest.mark.parametrize("name", list(polys_ok_np))
def test_polys_ok(name: str):
    poly, tolerance, expected = polys_ok_np[name]
    assert polylabel_ext_np(poly, tolerance) == expected


@pytest.mark.parametrize("name", list(polys_ok_np))
def test_polys_ok_unclosed(name: str):
    poly, tolerance, expected = polys_ok_np[name]
    assert polylabel_ext_np(poly[:-1], tolerance) == expected


@pytest.mark.parametrize("poly", polys_degenerate_np)
def test_polys_degenerate(poly: np.ndarray):
    # Note: also no exception in polylabel-rs
    assert polylabel_ext_np(poly, 0.5) == (0.0, 0.0)
