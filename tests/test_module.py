import os

import polylabel_pyo3


def test_module_doc():
    assert polylabel_pyo3.__doc__


def test_installed_path():
    assert len(polylabel_pyo3.__path__) == 1


def test_pyi_init_exists():
    path = polylabel_pyo3.__path__[0]
    assert os.path.isfile(os.path.join(path, "__init__.pyi"))
