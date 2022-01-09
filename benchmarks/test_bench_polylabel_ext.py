from polylabel_pyo3 import polylabel_ext


def test_ok_polys_ok(ok_bench_polys):
    for poly, tolerance in ok_bench_polys:
        assert polylabel_ext(poly, tolerance) != (0.0, 0.0)


def bench_oks(polys):
    for poly, tolerance in polys:
        polylabel_ext(poly, tolerance)


def test_bench_oks(benchmark, ok_bench_polys):
    benchmark.pedantic(
        bench_oks, (ok_bench_polys,), rounds=1000, iterations=5, warmup_rounds=10
    )
