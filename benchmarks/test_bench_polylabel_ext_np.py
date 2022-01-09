from typing import Tuple

import numpy as np
from polylabel_pyo3 import polylabel_ext_np

from .test_bench_polylabel_ext import bench_oks


def test_ok_polys_ok_np(ok_bench_polys_np):
    for poly, tolerance in ok_bench_polys_np:
        assert polylabel_ext_np(poly, tolerance) != (0.0, 0.0)


def bench_oks_np(polys: Tuple[np.ndarray, float]):
    for poly, tolerance in polys:
        polylabel_ext_np(poly, tolerance)


def test_bench_oks_np(benchmark, ok_bench_polys_np):
    benchmark.pedantic(
        bench_oks_np, (ok_bench_polys_np,), rounds=1000, iterations=5, warmup_rounds=10
    )


def test_bench_oks_np_generic(benchmark, ok_bench_polys_np):
    benchmark.pedantic(
        bench_oks, (ok_bench_polys_np,), rounds=1000, iterations=5, warmup_rounds=10
    )
