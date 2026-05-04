from objective import evaluate_schedule


def greedy_edd(p, w, d):
    """
    Greedy algorithm for 1 || sum w_j T_j based on the Earliest Due Date rule.

    Tasks are sorted by their due date d_j in non-decreasing order, which is the
    canonical EDD heuristic. The schedule is feasible-by-construction (machine
    runs continuously from t = 0) and the resulting weighted tardiness is then
    evaluated. EDD does not consider weights w_j or processing times p_j, so it
    is generally suboptimal but very fast: O(n log n).

    :param p: list of processing times
    :param w: list of weights
    :param d: list of due dates
    :return: tuple (order, cost)
    """
    n = len(p)
    if n == 0:
        return [], 0

    order = sorted(range(n), key=lambda j: d[j])
    cost = evaluate_schedule(order, p, w, d)
    return order, cost
