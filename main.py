from lab2.branch_and_bound import branch_and_bound_algorithm
from lab2.johnson import calculate_cmax, johnson_algorithm
import random

example_set = []
size_of_task_set = 7
random.seed(153)

for i in range(size_of_task_set):
    time1 = random.uniform(0, 50)
    time2 = random.uniform(0, 50)
    time1 = int(time1)
    time2 = int(time2)
    example_set.append((i, time1, time2))

johnson_order = johnson_algorithm(example_set)
johnson_cmax = calculate_cmax(johnson_order)

bnb_order, bnb_cmax = branch_and_bound_algorithm(example_set)

print("Example set: ", example_set)
print("Johnson order of tasks (by ID): ", [job[0] for job in johnson_order])
print("Johnson Cmax: ", johnson_cmax)
print("BnB order of tasks (by ID): ", [job[0] for job in bnb_order])
print("BnB Cmax: ", bnb_cmax)