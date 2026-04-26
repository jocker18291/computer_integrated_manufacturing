def _johnson_2_machines(jobs_2m):
    """Return Johnson order for 2-machine jobs in format (job_id, p1, p2)."""
    n1 = []
    n2 = []

    for job in jobs_2m:
        if job[1] <= job[2]:
            n1.append(job)
        else:
            n2.append(job)

    n1.sort(key=lambda x: x[1])
    n2.sort(key=lambda x: x[2], reverse=True)
    return n1 + n2


def johnson_algorithm(jobs, machine_count=2, multi_machine_mode="cds"):
    """
    Function implementing Johnson scheduling.

    For machine_count == 2 this is the exact Johnson algorithm (optimal for F2||Cmax).
    For machine_count > 2 and mode="cds" this uses the CDS heuristic
    (reduction to multiple 2-machine Johnson problems), so optimality is not guaranteed.

    :param jobs: list of tuples in format (job_id, p1, p2, ..., pm)
    :param machine_count: number of machines (m >= 2)
    :param multi_machine_mode: strategy for m > 2, currently only "cds"
    :return: list of tuples in scheduled order
    """
    if machine_count < 2:
        raise ValueError("machine_count must be at least 2")

    if not jobs:
        return []

    for job in jobs:
        if len(job) != machine_count + 1:
            raise ValueError(
                "Each job must have format (job_id, p1, ..., pm) matching machine_count"
            )

    if machine_count == 2:
        return _johnson_2_machines(jobs)

    if multi_machine_mode != "cds":
        raise ValueError("For machine_count > 2 only multi_machine_mode='cds' is supported")

    # Campbell-Dudek-Smith (CDS): build m-1 virtual 2-machine problems,
    # run Johnson on each and select the sequence with the best real Cmax.
    best_sequence = None
    best_cmax = float("inf")

    for k in range(1, machine_count):
        virtual_jobs = []
        for job in jobs:
            p_left = sum(job[1 : 1 + k])
            p_right = sum(job[1 + k : 1 + machine_count])
            virtual_jobs.append((job[0], p_left, p_right))

        virtual_order = _johnson_2_machines(virtual_jobs)
        ordered_ids = [job[0] for job in virtual_order]
        id_to_job = {job[0]: job for job in jobs}
        candidate_sequence = [id_to_job[job_id] for job_id in ordered_ids]

        candidate_cmax = calculate_cmax(candidate_sequence, machine_count=machine_count)
        if candidate_cmax < best_cmax:
            best_cmax = candidate_cmax
            best_sequence = candidate_sequence

    return best_sequence

def calculate_cmax(sequence, machine_count=2):
    """
    Function that calculates Cmax for a given sequence on m machines.

    :param sequence: list of tuples (job_id, p1, ..., pm)
    :param machine_count: number of machines (m >= 2)
    :return: Cmax value
    """
    if machine_count < 2:
        raise ValueError("machine_count must be at least 2")

    if not sequence:
        return 0

    completion_times = [0] * machine_count

    for job in sequence:
        if len(job) != machine_count + 1:
            raise ValueError(
                "Each job must have format (job_id, p1, ..., pm) matching machine_count"
            )

        completion_times[0] += job[1]
        for machine_idx in range(1, machine_count):
            completion_times[machine_idx] = (
                max(completion_times[machine_idx], completion_times[machine_idx - 1])
                + job[machine_idx + 1]
            )

    return completion_times[-1]
