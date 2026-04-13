import random
from algorithms import Tasks, carlier, schrage_no_queue, schrage_pmtn, schrage_queue

NUMBER_OF_TASKS = 20000


def build_tasks(number_of_tasks: int) -> list[Tasks]:
    random.seed(153)

    p_values = [random.randint(1, 29) for _ in range(number_of_tasks)]
    A = sum(p_values)
    r_values = [random.randint(1, A) for _ in range(number_of_tasks)]

    X = 29
    q_values = [random.randint(1, X) for _ in range(number_of_tasks)]

    return [Tasks(i, r_values[i], p_values[i], q_values[i]) for i in range(number_of_tasks)]


def main() -> None:
    tasks = build_tasks(NUMBER_OF_TASKS)

    _, sch_no_q = schrage_no_queue(tasks)
    print(f"Schrage no queue: {sch_no_q}")

    _, sch_q = schrage_queue(tasks)
    print(f"Schrage queue: {sch_q}")

    sch_pmtn = schrage_pmtn(tasks)
    print(f"Schrage PMTN (LB): {sch_pmtn}")

    carl = carlier(tasks)
    print(f"Carlier: {carl}")


if __name__ == "__main__":
    main()