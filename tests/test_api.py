import inspect
import os

import polylabel_pyo3
import pytest
from polylabel_pyo3 import PolylabelError, PolylabelShapeError


def test_module_doc():
    assert polylabel_pyo3.__doc__


def test_installed_path():
    assert len(polylabel_pyo3.__path__) == 1


def test_pyi_init_exists():
    path = polylabel_pyo3.__path__[0]
    assert os.path.isfile(os.path.join(path, "__init__.pyi"))


@pytest.mark.parametrize("e_type", [PolylabelError, PolylabelShapeError])
def test_exceptions(e_type):
    try:
        raise PolylabelError("test")
    except PolylabelError as e:
        assert e.args == ("test",)


@pytest.mark.parametrize("func_name", ["polylabel_ext", "polylabel_ext_np"])
def test_function_doc(func_name: str):
    func = getattr(polylabel_pyo3, func_name)
    assert func.__doc__


@pytest.mark.parametrize("func_name", ["polylabel_ext", "polylabel_ext_np"])
def test_function_sig(func_name: str):
    func = getattr(polylabel_pyo3, func_name)
    sig = inspect.signature(func)
    sig.bind([], 0.1)
    sig.bind(exterior=[], tolerance=0.1)
    sig.bind([], tolerance=0.1)
