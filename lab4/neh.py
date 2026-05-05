from objective import calculate_cmax, completion_matrix


def _initial_job_order(processing_times):
    weighted = []
    for job_idx, times in enumerate(processing_times):
        weighted.append((sum(times), job_idx))
    weighted.sort(reverse=True)
    return [job_idx for _, job_idx in weighted]


def _best_insertion(sequence, job_idx, processing_times):
    best_sequence = None
    best_cmax = float("inf")

    for pos in range(len(sequence) + 1):
        candidate = sequence[:pos] + [job_idx] + sequence[pos:]
        cmax = calculate_cmax(candidate, processing_times)
        if cmax < best_cmax:
            best_cmax = cmax
            best_sequence = candidate

    return best_sequence, best_cmax


def neh(processing_times):
    """
    Base NEH algorithm for FP||Cmax.
    """
    sequence = []
    for job_idx in _initial_job_order(processing_times):
        sequence, _ = _best_insertion(sequence, job_idx, processing_times)
    return sequence, calculate_cmax(sequence, processing_times)


def _critical_path_operations(sequence, processing_times):
    """
    Return operations (machine, pos, job_idx, duration) on one critical path.
    """
    if not sequence:
        return []

    c = completion_matrix(sequence, processing_times)
    machine = len(c) - 1
    pos = len(sequence) - 1
    operations = []

    while True:
        job_idx = sequence[pos]
        duration = processing_times[job_idx][machine]
        operations.append((machine, pos, job_idx, duration))

        if machine == 0 and pos == 0:
            break
        if machine == 0:
            pos -= 1
            continue
        if pos == 0:
            machine -= 1
            continue

        if c[machine - 1][pos] >= c[machine][pos - 1]:
            machine -= 1
        else:
            pos -= 1

    operations.reverse()
    return operations


def _choose_job_rule_1(sequence, inserted_job, processing_times):
    """
    Rule 1: choose job with the longest operation on the critical path.
    """
    critical_ops = _critical_path_operations(sequence, processing_times)
    excluded = inserted_job

    best_job = None
    best_duration = -1
    for _, _, job_idx, duration in critical_ops:
        if job_idx == excluded:
            continue
        if duration > best_duration:
            best_duration = duration
            best_job = job_idx

    return best_job


def _neh_plus(processing_times, choose_job_fn):
    """
    Generic NEH+: after each regular insertion,
    remove one already assigned job and reinsert it.
    """
    sequence = []
    for job_idx in _initial_job_order(processing_times):
        sequence, _ = _best_insertion(sequence, job_idx, processing_times)

        chosen = choose_job_fn(sequence, job_idx, processing_times)
        if chosen is None:
            continue

        reduced = [j for j in sequence if j != chosen]
        sequence, _ = _best_insertion(reduced, chosen, processing_times)

    return sequence, calculate_cmax(sequence, processing_times)


def neh_plus_rule_1(processing_times):
    return _neh_plus(processing_times, _choose_job_rule_1)
