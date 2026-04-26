from __future__ import annotations
from typing import Sequence
from lab2.johnson import johnson_algorithm

Job = tuple[int, int, int]

def calculate_cmax(sequence: Sequence[Job]) -> int:
    t1 = 0
    t2 = 0

    for _, p1, p2 in sequence:
        t1 += p1
        t2 = max(t1, t2) + p2

    return t2

def lower_bound(t1: int, t2: int, remaining_jobs: Sequence[Job]) -> int:
    """
    Lower bound for partial solution.

    Combines three admissible bounds:
    - machine 2 workload still to process,
    - machine 1 finish plus minimum tail on machine 2,
    - earliest possible start of first remaining op on machine 2.
    """
    if not remaining_jobs:
        return t2

    sum_p1 = sum(job[1] for job in remaining_jobs)
    sum_p2 = sum(job[2] for job in remaining_jobs)
    min_p1 = min(job[1] for job in remaining_jobs)
    min_p2 = min(job[2] for job in remaining_jobs)

    lb_m2_load = t2 + sum_p2
    lb_m1_tail = t1 + sum_p1 + min_p2
    lb_first_release_to_m2 = max(t2, t1 + min_p1) + sum_p2

    return max(lb_m2_load, lb_m1_tail, lb_first_release_to_m2)


def state_after_prefix(prefix: Sequence[Job]) -> tuple[int, int]:
    """Return completion times on machine 1 and 2 after prefix."""
    t1 = 0
    t2 = 0
    for _, p1, p2 in prefix:
        t1 += p1
        t2 = max(t1, t2) + p2
    return t1, t2


def branch_and_bound_algorithm(jobs: Sequence[Job]) -> tuple[list[Job], int]:
    """
    Returns best sequence and corresponding Cmax.
    """
    jobs = list(jobs)
    if not jobs:
        return [], 0

    # Good initial upper bound from Johnson heuristic.
    best_sequence = list(johnson_algorithm(jobs))
    best_cmax = calculate_cmax(best_sequence)

    def recurse(prefix: list[Job], remaining: list[Job]) -> None:
        nonlocal best_sequence, best_cmax

        t1, t2 = state_after_prefix(prefix)
        lb = lower_bound(t1, t2, remaining)
        if lb >= best_cmax:
            return

        if not remaining:
            current_cmax = t2
            if current_cmax < best_cmax:
                best_cmax = current_cmax
                best_sequence = prefix.copy()
            return

        # Build a strong node upper bound by completing with Johnson order.
        completion = list(johnson_algorithm(remaining))
        candidate_sequence = prefix + completion
        candidate_cmax = calculate_cmax(candidate_sequence)
        if candidate_cmax < best_cmax:
            best_cmax = candidate_cmax
            best_sequence = candidate_sequence

        # Branch in Johnson-like order to improve incumbent quickly.
        ordered_remaining = completion
        for next_job in ordered_remaining:
            new_prefix = prefix + [next_job]
            new_remaining = [job for job in remaining if job[0] != next_job[0]]
            recurse(new_prefix, new_remaining)

    recurse([], jobs)
    return best_sequence, best_cmax


if __name__ == "__main__":
    sample_jobs = [
        (1, 4, 1),
        (2, 4, 3),
        (3, 1, 2),
        (4, 5, 1),
    ]
    best_seq, best_cmax = branch_and_bound_algorithm(sample_jobs)
    print("Best sequence:", best_seq)
    print("Cmax:", best_cmax)