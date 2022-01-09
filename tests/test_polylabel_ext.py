import pytest
from polylabel_pyo3 import polylabel_ext

from .fixtures import Poly, polys_degenerate, polys_ok


def test_empty():
    assert polylabel_ext([], 0.1) == (0.0, 0.0)


def test_wrong_shape():
    with pytest.raises(IndexError):
        polylabel_ext([(1.0,)], 1.0)


def test_wrong_type():
    with pytest.raises(TypeError):
        polylabel_ext([(0.0, 1.0), ("a", 2.0)], 1.0)


def test_wrong_shape_and_type():
    with pytest.raises(TypeError):
        polylabel_ext(None, 2.0)


def test_iterable_lists():
    iterable = (c for c in ([0, 1], [1, 0]))
    polylabel_ext(iterable, 1.0)


@pytest.mark.parametrize("name", list(polys_ok))
def test_polys_ok(name: str):
    poly, tolerance, expected = polys_ok[name]
    assert polylabel_ext(poly, tolerance) == expected


@pytest.mark.parametrize("name", list(polys_ok))
def test_polys_ok_unclosed(name: str):
    poly, tolerance, expected = polys_ok[name]
    assert polylabel_ext(poly[:-1], tolerance) == expected


@pytest.mark.parametrize("name", list(polys_ok))
def test_polys_ok_unclosed_iter_map(name: str):
    poly, tolerance, expected = polys_ok[name]
    poly = ({0: c[0], 1: c[1]} for c in poly[:-1])
    assert polylabel_ext(poly, tolerance) == expected


@pytest.mark.parametrize("poly", polys_degenerate)
def test_polys_degenerate(poly: Poly):
    # Note: also no exception in polylabel-rs
    assert polylabel_ext(poly, 0.5) == (0.0, 0.0)
