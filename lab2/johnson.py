def johnson_algorithm(jobs):
    """
    Function implementing Johnson algorithm.
    :param jobs: list of tuples in format (job_id, time_machine_1, time_machine_2)
    :return: List of tuples in optimal order
    """

    n1 = []
    n2 = []

    # 1. We divide on sets N1 and N2
    for job in jobs:
        if job[1] <= job[2]:
            n1.append(job)
        else:
            n2.append(job)
    
    # 2. Sorting N1 in ascending order on machine 1 (index 1)
    n1.sort(key=lambda x: x[1])

    # 3. Sorting N2 in descending order on machine 2 (index 2)
    n2.sort(key=lambda x: x[2], reverse=True)

    # 4. We sum sets
    return n1 + n2
    