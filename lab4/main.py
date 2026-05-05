import time

from instance import generate_instance
from neh import neh, neh_plus_rule_1


def _measure(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def run_case(label, processing_times):
    n = len(processing_times)
    m = len(processing_times[0]) if processing_times else 0

    print(f"\n=== {label} ===")
    print(f"n = {n}, m = {m}")
    print("Processing matrix p[j][i]:")
    for j, row in enumerate(processing_times):
        print(f"job {j:>2}: {row}")

    (neh_result, neh_time) = _measure(neh, processing_times)
    neh_sequence, neh_cmax = neh_result
    print(
        f"NEH                 : Cmax = {neh_cmax:>6}   "
        f"pi = {neh_sequence}   time = {neh_time:.6f}s"
    )

    (r1_result, r1_time) = _measure(neh_plus_rule_1, processing_times)
    r1_sequence, r1_cmax = r1_result
    print(
        f"NEH+ (rule 1)       : Cmax = {r1_cmax:>6}   "
        f"pi = {r1_sequence}   time = {r1_time:.6f}s"
    )

if __name__ == "__main__":
    n = 10
    m = 5
    seed = 42

    processing_times = generate_instance(n=n, m=m, seed=seed, p_min=1, p_max=29)
    run_case("Generated FP||Cmax instance", processing_times)
