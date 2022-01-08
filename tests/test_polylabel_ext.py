import pytest
from polylabel_pyo3 import polylabel_ext

from .fixtures import Poly, polys_degenerate, polys_ok


def test_empty():
    assert polylabel_ext([], 0.1) == (0.0, 0.0)


@pytest.mark.parametrize("name", list(polys_ok))
def test_polys_ok(name: str):
    poly, tolerance, expected = polys_ok[name]
    assert polylabel_ext(poly, tolerance) == expected


@pytest.mark.parametrize("poly", polys_degenerate)
def test_polys_degenerate(poly: Poly):
    # Note: also no exception in polylabel-rs
    assert polylabel_ext(poly, 0.5) == (0.0, 0.0)
