from dynamic_bitmask import dp_total_weighted_tardiness, generate_instance, get_optimal_order


def solve_and_print(label, p, w, d):
    n = len(p)
    dp, subset_processing_sum = dp_total_weighted_tardiness(p, w, d)
    optimal_cost = dp[(1 << n) - 1]
    order = get_optimal_order(p, w, d, dp, subset_processing_sum)

    print(f"\n=== {label} ===")
    print(f"p = {p}")
    print(f"w = {w}")
    print(f"d = {d}")
    print(f"Optimal cost: {optimal_cost}")
    print(f"Task order:   {order}")


if __name__ == "__main__":
    n = 10
    Z = 42

    p, w, d = generate_instance(n, Z, X="A")
    A = sum(p)
    solve_and_print(f"X = A = {A}", p, w, d)

    p, w, d = generate_instance(n, Z, X=29)
    solve_and_print("X = 29", p, w, d)
