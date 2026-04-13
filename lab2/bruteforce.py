import itertools

def brute_force_algorithm(jobs):
    best_sequence = None
    best_cmax = float('inf')

    for perm in itertools.permutations(jobs):
        cmax = calculate_cmax(perm)

        if cmax < best_cmax:
            best_cmax = cmax
            best_sequence = perm

    return list(best_sequence), best_cmax

def calculate_cmax(sequence):
    t1 = 0
    t2 = 0

    for job in sequence:
        t1 += job[1]
        t2 = max(t1, t2) + job[2]

    return t2

if __name__ == "__main__":
    jobs = [
        (1, 4, 1),
        (2, 4, 3),
        (3, 1, 2),
        (4, 5, 1)
    ]

    best_seq, best_cmax = brute_force_algorithm(jobs)

    print("Best sequence:", best_seq)
    print("Cmax:", best_cmax)