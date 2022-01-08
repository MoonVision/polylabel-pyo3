from typing import Dict, List, Tuple

from .polys import poly0 as poly_L
from .polys import poly1
from .polys import poly2 as poly_concave
from .polys import poly3 as poly_london

Poly = List[Tuple[float, float]]
# polygon, tolerance, expected
PolyTest = Tuple[Poly, float, Tuple[float, float]]


# all polys are closed, i.e. last point is first point
polys_ok: Dict[str, PolyTest] = dict(
    [
        ("poly_L", (poly_L, 0.1, (0.5625, 0.5625))),
        ("poly1", (poly1, 10.0, (59.35615556364569, 121.83919629746435))),
        (
            "poly_concave",
            (poly_concave, 1.0, (16.89453125, 16.89453125)),
        ),  # Note: own expected
        (
            "poly_london",
            (poly_london, 0.001, (-0.45556816445920356, 51.54848888202887)),
        ),
    ]
)


polys_degenerate: List[Poly] = [
    # degenerate_polygon_test in polylabel-rs
    [(0.0, 0.0), (1.0, 0.0), (2.0, 0.0), (0.0, 0.0)],
    # degenerate_polygon_test2 in polylabel-rs
    [(0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (1.0, 0.0), (0.0, 0.0)],
]
