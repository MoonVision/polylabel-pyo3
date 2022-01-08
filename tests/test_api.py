import os

import polylabel_pyo3
import pytest
from polylabel_pyo3 import PolylabelError


def test_module_doc():
    assert polylabel_pyo3.__doc__


def test_installed_path():
    assert len(polylabel_pyo3.__path__) == 1


def test_pyi_init_exists():
    path = polylabel_pyo3.__path__[0]
    assert os.path.isfile(os.path.join(path, "__init__.pyi"))


def test_exception():
    try:
        raise PolylabelError("test")
    except PolylabelError as e:
        assert e.args == ("test",)


@pytest.mark.parametrize("func_name", ["polylabel_ext"])
def test_function_doc(func_name: str):
    func = getattr(polylabel_pyo3, func_name)
    assert func.__doc__
