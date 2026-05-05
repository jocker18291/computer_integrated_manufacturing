import random


def generate_instance(n, m, seed, p_min=1, p_max=29):
    """
    Generate FP||Cmax instance.

    :param n: number of jobs
    :param m: number of machines
    :param seed: seed
    :param p_min: minimum processing time
    :param p_max: maximum processing time
    :return: processing matrix p[j][i] for job j on machine i
    """
    if n <= 0:
        raise ValueError("n must be positive")
    if m <= 0:
        raise ValueError("m must be positive")
    if p_min <= 0 or p_max <= 0 or p_min > p_max:
        raise ValueError("Invalid processing time range")

    random.seed(seed)
    return [[random.randint(p_min, p_max) for _ in range(m)] for _ in range(n)]
