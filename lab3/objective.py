def evaluate_schedule(order, p, w, d):
    """
    Compute Total Weighted Tardiness for a given task order.

    Implements the objective function F(pi) = sum_j w_{pi(j)} * T_{pi(j)},
    where T_{pi(j)} = max(C_{pi(j)} - d_{pi(j)}, 0) and the machine works
    continuously starting from time 0 (S_{pi(j)} = C_{pi(j-1)}).

    :param order: permutation of task indices (0-based)
    :param p: list of processing times
    :param w: list of weights
    :param d: list of due dates
    :return: value of F(pi)
    """
    completion_time = 0
    total = 0
    for j in order:
        completion_time += p[j]
        tardiness = completion_time - d[j]
        if tardiness > 0:
            total += w[j] * tardiness
    return total
