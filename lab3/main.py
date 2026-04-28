from dynamic_recurrence import dp_total_weighted_tardiness
import random

if __name__ == "__main__":

    size = 10

    p = [random.randint(1, 100) for _ in range(size)]
    w = [random.randint(1, 100) for _ in range(size)]
    d = [random.randint(1, 100) for _ in range(size)]

    result = dp_total_weighted_tardiness(p, w, d)
    print(f"Processing times: {p}")
    print(f"Weights: {w}")
    print(f"Due dates: {d}")
    print(f"Minimum total weighted tardiness: {result}")
