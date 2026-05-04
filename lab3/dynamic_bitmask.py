import random


def _validate_instance(p, w, d):
    if not (isinstance(p, list) and isinstance(w, list) and isinstance(d, list)):
        raise TypeError("p, w, d must be lists of integers.")

    if len(p) == 0:
        raise ValueError("At least one task is required.")

    if not (len(p) == len(w) == len(d)):
        raise ValueError("p, w, d must have the same length.")

    for name, values in (("p", p), ("w", w), ("d", d)):
        for value in values:
            if not isinstance(value, int):
                raise TypeError(f"All values in {name} must be integers.")

    if any(value <= 0 for value in p):
        raise ValueError("Processing times p must be positive integers.")

    if any(value <= 0 for value in w):
        raise ValueError("Weights w must be positive integers.")

    if any(value <= 0 for value in d):
        raise ValueError("Due dates d must be positive integers.")


def generate_instance(n, Z, X):
    random.seed(Z)
    p = [random.randint(1, 29) for _ in range(n)]
    A = sum(p)
    w = [random.randint(1, 9) for _ in range(n)]
    upper = A if X == "A" else X
    d = [random.randint(1, upper) for _ in range(n)]
    return p, w, d


def get_optimal_order(p, w, d, dp, subset_processing_sum):
    n = len(p)
    mask = (1 << n) - 1
    order = []

    while mask:
        for j in range(n):
            if mask & (1 << j):
                prev_mask = mask ^ (1 << j)
                tardiness = max(subset_processing_sum[mask] - d[j], 0)
                if dp[mask] == dp[prev_mask] + w[j] * tardiness:
                    order.append(j)
                    mask = prev_mask
                    break

    order.reverse()
    return order


def dp_total_weighted_tardiness(p, w, d):
    _validate_instance(p, w, d)

    n = len(p)
    max_mask = 1 << n

    dp = [float("inf")] * max_mask
    subset_processing_sum = [0] * max_mask
    dp[0] = 0

    for mask in range(1, max_mask):
        lsb = mask & -mask
        job_index = lsb.bit_length() - 1
        subset_processing_sum[mask] = subset_processing_sum[mask ^ lsb] + p[job_index]

    for mask in range(1, max_mask):
        completion_time = subset_processing_sum[mask]
        remaining = mask

        while remaining:
            bit = remaining & -remaining
            job_index = bit.bit_length() - 1
            prev_mask = mask ^ bit

            tardiness = max(completion_time - d[job_index], 0)
            candidate = dp[prev_mask] + w[job_index] * tardiness
            if candidate < dp[mask]:
                dp[mask] = candidate

            remaining ^= bit

    return dp, subset_processing_sum

