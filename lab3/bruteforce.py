import itertools

from objective import evaluate_schedule


def brute_force(p, w, d):
    """
    Complete enumeration (Brute Force) for 1 || sum w_j T_j.

    Iterates over all n! permutations of task indices and returns the one
    with the minimal Total Weighted Tardiness. Time complexity is O(n! * n),
    so this is intended only for small instances (roughly n <= 10).

    :param p: list of processing times
    :param w: list of weights
    :param d: list of due dates
    :return: tuple (best_order, best_cost)
    """
    n = len(p)
    if n == 0:
        return [], 0

    best_order = None
    best_cost = float("inf")

    for perm in itertools.permutations(range(n)):
        cost = evaluate_schedule(perm, p, w, d)
        if cost < best_cost:
            best_cost = cost
            best_order = perm

    return list(best_order), best_cost
