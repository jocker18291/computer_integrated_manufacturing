from lab2.branch_and_bound import branch_and_bound_algorithm
from lab2.johnson import calculate_cmax, johnson_algorithm
from lab2.bruteforce import brute_force_algorithm
import random

example_set = []
size_of_task_set = 7
machine_count = 2
random.seed(153)

for i in range(size_of_task_set):
    processing_times = [int(random.uniform(0, 50)) for _ in range(machine_count)]
    example_set.append((i, *processing_times))

johnson_order = johnson_algorithm(example_set, machine_count=machine_count)
johnson_cmax = calculate_cmax(johnson_order, machine_count=machine_count)

print("Example set: ", example_set)
print("Machine count:", machine_count)
print("Johnson order of tasks (by ID): ", [job[0] for job in johnson_order])
print("Johnson Cmax: ", johnson_cmax)


if machine_count == 2:
    bnb_order, bnb_cmax = branch_and_bound_algorithm(example_set)

    best_seq, best_cmax = brute_force_algorithm(example_set)

    print("Brute Force: Sequence", [job[0] for job in best_seq])
    print("Brute Force: Cmax:", best_cmax)
    print("BnB order of tasks (by ID): ", [job[0] for job in bnb_order])
    print("BnB Cmax: ", bnb_cmax)
else:

    print("Brute Force and Branch & Bound are currently implemented only for 2 machines.")