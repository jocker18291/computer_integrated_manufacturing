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

def calculate_cmax(sequence):
    """
    Function that calculates Cmax time for given sequence of tasks
    """
    t1 = 0 # time to finish the operation on machine 1
    t2 = 0 # time to finish the operation on machine 2

    for job in sequence:
        t1 += job[1]
        # The machine 2 can start working on the task only when the prior one is finished AND when the task is gone from machine 1
        t2 = max(t1, t2) + job[2]
    
    return t2