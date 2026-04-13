import heapq
from copy import deepcopy
from dataclasses import dataclass
from math import inf


@dataclass
class Tasks:
    id: int
    r_j: int
    p_j: int
    q_j: int


def calculate_cmax(pi: list[Tasks]) -> int:
    if not pi:
        return 0

    S = max(pi[0].r_j, 0)
    C = S + pi[0].p_j
    cmax = C + pi[0].q_j

    for j in range(1, len(pi)):
        S = max(pi[j].r_j, C)
        C = S + pi[j].p_j
        cmax = max(cmax, C + pi[j].q_j)

    return cmax


def schrage_no_queue(tasks: list[Tasks]) -> tuple[list[Tasks], int]:
    if not tasks:
        return [], 0

    N = tasks.copy()
    G = []
    t = min(task.r_j for task in N)
    pi = []

    while G or N:
        moved = True
        while moved:
            moved = False
            candidate = None
            for task in N:
                if task.r_j <= t:
                    if candidate is None or task.r_j < candidate.r_j:
                        candidate = task

            if candidate is not None:
                G.append(candidate)
                N.remove(candidate)
                moved = True

        if G:
            current = max(G, key=lambda task: task.q_j)
            G.remove(current)
            pi.append(current)
            t = t + current.p_j
        else:
            t = min(task.r_j for task in N)

    cmax = calculate_cmax(pi)

    return pi, cmax


def schrage_queue(tasks: list[Tasks]) -> tuple[list[Tasks], int]:
    if not tasks:
        return [], 0

    Q_N: list[tuple[int, int, Tasks]] = []
    for task in tasks:
        heapq.heappush(Q_N, (task.r_j, task.id, task))

    Q_G: list[tuple[int, int, Tasks]] = []

    t = Q_N[0][0]
    pi: list[Tasks] = []

    while Q_G or Q_N:
        while Q_N and Q_N[0][0] <= t:
            _, _, task = heapq.heappop(Q_N)
            heapq.heappush(Q_G, (-task.q_j, task.id, task))
        if Q_G:
            _, _, task = heapq.heappop(Q_G)
            pi.append(task)
            t += task.p_j
        else:
            t = Q_N[0][0]
    cmax = calculate_cmax(pi)
    return pi, cmax


def schrage_pmtn(tasks: list[Tasks]) -> int:
    if not tasks:
        return 0

    Q_N: list[tuple[int, int, Tasks]] = []
    for task in tasks:
        heapq.heappush(Q_N, (task.r_j, task.id, task))

    Q_G: list[tuple[int, int, Tasks, int]] = []

    t = Q_N[0][0]
    cmax = 0

    current: Tasks | None = None
    current_rem = 0

    def move_ready_jobs(now: int) -> None:
        while Q_N and Q_N[0][0] <= now:
            _, _, job = heapq.heappop(Q_N)
            heapq.heappush(Q_G, (-job.q_j, job.id, job, job.p_j))

    while Q_N or Q_G or current is not None:
        if current is None:
            if not Q_G:
                t = Q_N[0][0]
                move_ready_jobs(t)
            _, _, current, current_rem = heapq.heappop(Q_G)
            continue

        next_r = Q_N[0][0] if Q_N else inf
        finish_time = t + current_rem

        if next_r < finish_time:
            current_rem -= next_r - t
            t = next_r
            move_ready_jobs(t)

            if Q_G and (-Q_G[0][0]) > current.q_j:
                heapq.heappush(Q_G, (-current.q_j, current.id, current, current_rem))
                _, _, current, current_rem = heapq.heappop(Q_G)
        else:
            t = finish_time
            cmax = max(cmax, t + current.q_j)
            current = None
            current_rem = 0
            move_ready_jobs(t)

    return cmax


def carlier(tasks: list[Tasks]) -> int:
    UB = inf
    best_pi: list[Tasks] = []

    def recurse(J: list[Tasks]):
        nonlocal UB, best_pi

        pi, _ = schrage_queue(J)
        U = calculate_cmax(pi)
        if U < UB:
            UB = U
            best_pi = pi

        LB = schrage_pmtn(J)
        if LB >= UB:
            return

        t = 0
        S = {}
        C = {}
        C_q = {}
        for job in pi:
            t = max(t, job.r_j)
            S[job.id] = t
            t = t + job.p_j
            C[job.id] = t
            C_q[job.id] = t + job.q_j
        Cmax_val = max(C_q.values())

        b_idx = max(i for i, job in enumerate(pi) if C_q[job.id] == Cmax_val)

        sum_p = 0
        q_b = pi[b_idx].q_j
        a_idx = None
        for i in range(b_idx, -1, -1):
            sum_p += pi[i].p_j
            if Cmax_val == pi[i].r_j + sum_p + q_b:
                a_idx = i
        if a_idx is None:
            return

        c_idx = None
        for i in range(b_idx - 1, a_idx - 1, -1):
            if pi[i].q_j < q_b:
                c_idx = i
                break
        if c_idx is None:
            return

        K = pi[c_idx + 1 : b_idx + 1]
        r_hat = min(job.r_j for job in K)
        q_hat = min(job.q_j for job in K)
        p_hat = sum(job.p_j for job in K)

        c_job_id = pi[c_idx].id

        def find_job(lst: list[Tasks], job_id: int) -> Tasks:
            for job in lst:
                if job.id == job_id:
                    return job
            raise KeyError(job_id)

        J1 = deepcopy(J)
        jc1 = find_job(J1, c_job_id)
        old_r = jc1.r_j
        jc1.r_j = max(jc1.r_j, r_hat + p_hat)
        if schrage_pmtn(J1) < UB:
            recurse(J1)
        jc1.r_j = old_r

        J2 = deepcopy(J)
        jc2 = find_job(J2, c_job_id)
        old_q = jc2.q_j
        jc2.q_j = max(jc2.q_j, q_hat + p_hat)
        if schrage_pmtn(J2) < UB:
            recurse(J2)
        jc2.q_j = old_q

    recurse(tasks)
    return UB