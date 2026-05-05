def completion_matrix(order, processing_times):
    """
    Build completion-time matrix C for a permutation.

    C[i][k] = completion time on machine i for k-th job in.
    """
    if not order:
        return []

    machine_count = len(processing_times[0])
    job_count = len(order)
    c = [[0] * job_count for _ in range(machine_count)]

    for pos, job_idx in enumerate(order):
        for machine in range(machine_count):
            from_prev_machine = c[machine - 1][pos] if machine > 0 else 0
            from_prev_job = c[machine][pos - 1] if pos > 0 else 0
            start = max(from_prev_machine, from_prev_job)
            c[machine][pos] = start + processing_times[job_idx][machine]

    return c


def calculate_cmax(order, processing_times):
    """
    Calculate Cmax for a permutation.
    """
    if not order:
        return 0
    c = completion_matrix(order, processing_times)
    return c[-1][-1]
