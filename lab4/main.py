import time
import random

from instance import generate_instance
from neh import neh, neh_plus_rule_1
from insa import INSA


def _measure(fn, *args):
    start = time.perf_counter()
    result = fn(*args)
    elapsed = time.perf_counter() - start
    return result, elapsed


def generate_job_shop_instance(n, m, seed, p_min=1, p_max=29):
    random.seed(seed)
    jobs_data = []
    for _ in range(n):
        max_ops = max(1, int(m * 1.2))
        num_operations = random.randint(1, max_ops)
        operations = []
        for _ in range(num_operations):
            machine_id = random.randint(0, m - 1)
            processing_time = random.randint(p_min, p_max)
            operations.append((machine_id, processing_time))
        jobs_data.append(operations)
    return jobs_data


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
        f"NEH                  : Cmax = {neh_cmax:>6}   "
        f"pi = {neh_sequence}   time = {neh_time:.6f}s"
    )

    (r1_result, r1_time) = _measure(neh_plus_rule_1, processing_times)
    r1_sequence, r1_cmax = r1_result
    print(
        f"NEH+ (rule 1)        : Cmax = {r1_cmax:>6}   "
        f"pi = {r1_sequence}   time = {r1_time:.6f}s"
    )

    # Konwersja danych z Flow Shop na format Job Shop, aby sprawdzić INSA na danych kolegów
    insa_jobs_data = [
        [(machine_id, time) for machine_id, time in enumerate(job_times)]
        for job_times in processing_times
    ]

    (insa_result, insa_time) = _measure(INSA, insa_jobs_data)
    insa_cmax, insa_schedule = insa_result
    print(
        f"INSA (na Flow Shop)  : Cmax = {insa_cmax:>6}   "
        f"time = {insa_time:.6f}s"
    )


def run_job_shop_case(label, jobs_data):
    print(f"\n=== {label} ===")
    n = len(jobs_data)
    print(f"n = {n}")
    for j, job in enumerate(jobs_data):
        print(f"job {j:>2}: {job}")

    (insa_result, insa_time) = _measure(INSA, jobs_data)
    insa_cmax, insa_schedule = insa_result
    print(
        f"\nINSA (na Job Shop)   : Cmax = {insa_cmax:>6}   "
        f"time = {insa_time:.6f}s"
    )
# ------------------------------------------------------------------


if __name__ == "__main__":
    n = 10
    m = 5
    seed = 42

    # 1. Kod kolegów (3.0/4.0) - generuje Flow Shop i uruchamia NEH, NEH+ oraz INSA
    processing_times = generate_instance(n=n, m=m, seed=seed, p_min=1, p_max=29)
    run_case("Dane Flow Shop (FP||Cmax) - Porownanie NEH i INSA", processing_times)

    # 2. Twój dodatek (5.0) - generuje prawidziwy Job Shop i uruchamia INSA
    job_shop_data = generate_job_shop_instance(n=n, m=m, seed=seed, p_min=1, p_max=29)
    run_job_shop_case("Dane Job Shop (J||Cmax) - Wymog na ocene 5.0", job_shop_data)