import math
import random
from typing import List, Tuple

import numpy as np
import pytest

Poly = List[Tuple[float, float]]


def rand_contour(num_vertices: int, width: int = 255, height: int = 255) -> Poly:
    cx, cy, r = (
        random.randint(2, width),
        random.randint(2, height),
        random.randint(2, width + height) // 4,
    )

    contour = []
    alpha_range = 2 * math.pi / num_vertices
    for k in range(num_vertices - 1):
        angle = k * alpha_range + random.random() * alpha_range
        x, y = r * math.cos(angle), r * math.sin(angle)
        contour.append((cx + x, cy + y))

    return contour


@pytest.fixture()
def ok_bench_polys() -> List[Tuple[Poly, float]]:
    random.seed("42", version=2)
    verts_tols = [(10, 1.0), (4, 0.1), (100, 0.01), (1000, 1.0), (100, 0.01)]
    polys = [(rand_contour(num), tol) for num, tol in verts_tols]
    return polys


@pytest.fixture()
def ok_bench_polys_np(request) -> Tuple[np.ndarray, float]:
    polys = request.getfixturevalue("ok_bench_polys")
    polys = [(np.array(c, dtype=np.float64), t) for c, t in polys]
    return polys
