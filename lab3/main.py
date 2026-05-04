import time

from bruteforce import brute_force
from dynamic_bitmask import (
    dp_total_weighted_tardiness,
    generate_instance,
    get_optimal_order,
)
from greedy import greedy_edd
from objective import evaluate_schedule


def _measure(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def solve_and_print(label, p, w, d, run_brute_force=True):
    n = len(p)
    print(f"\n=== {label} ===")
    print(f"n = {n}")
    print(f"p = {p}")
    print(f"w = {w}")
    print(f"d = {d}")

    (greedy_order, greedy_cost), greedy_time = _measure(greedy_edd, p, w, d)
    print(
        f"Greedy (EDD)     : F = {greedy_cost:>8}   order = {greedy_order}"
        f"   time = {greedy_time:.6f}s"
    )

    if run_brute_force:
        (bf_order, bf_cost), bf_time = _measure(brute_force, p, w, d)
        print(
            f"Brute force      : F = {bf_cost:>8}   order = {bf_order}"
            f"   time = {bf_time:.6f}s"
        )
    else:
        bf_cost = None
        print("Brute force      : skipped (n is too large)")

    (dp_data, dp_time) = _measure(dp_total_weighted_tardiness, p, w, d)
    dp, subset_processing_sum = dp_data
    dp_cost = dp[(1 << n) - 1]
    dp_order = get_optimal_order(p, w, d, dp, subset_processing_sum)
    print(
        f"Dynamic prog.    : F = {dp_cost:>8}   order = {dp_order}"
        f"   time = {dp_time:.6f}s"
    )

    if bf_cost is not None and bf_cost != dp_cost:
        raise AssertionError(
            f"Mismatch between brute force ({bf_cost}) and DP ({dp_cost})"
        )
    if greedy_cost < dp_cost:
        raise AssertionError(
            f"Greedy beat the optimum ({greedy_cost} < {dp_cost}) - bug in DP"
        )


def run_pdf_example():
    """Reproduce the worked example from the lab handout (Tabela 1)."""
    p = [3, 4, 2, 2, 3, 4]
    w = [3, 2, 1, 2, 4, 2]
    d = [3, 10, 6, 15, 21, 16]
    expected_order = [0, 1, 2, 3, 4, 5]
    expected_cost = 7

    cost = evaluate_schedule(expected_order, p, w, d)
    print("\n=== PDF example (Tabela 1) ===")
    print(f"order   = {expected_order}")
    print(f"F(pi)   = {cost} (expected {expected_cost})")
    assert cost == expected_cost, "Objective function does not match the handout"

    solve_and_print("PDF instance, all algorithms", p, w, d)


if __name__ == "__main__":
    run_pdf_example()

    n = 10
    Z = 42

    p, w, d = generate_instance(n, Z, X="A")
    A = sum(p)
    solve_and_print(f"Generated instance, n = {n}, X = A = {A}", p, w, d)

    p, w, d = generate_instance(n, Z, X=29)
    solve_and_print(f"Generated instance, n = {n}, X = 29", p, w, d)
