from lab2.johnson import johnson_algorithm, calculate_cmax
import random

example_set = []
size_of_task_set = 5;

for i in range(size_of_task_set):
    time1 = random.uniform(0, 50)
    time2 = random.uniform(0, 50)
    time1 = int(time1)
    time2 = int(time2)
    example_set.append([i, time1, time2])

optimum_order = johnson_algorithm(example_set)
cmax = calculate_cmax(optimum_order)

print("Example set: ", example_set)
print("Optimum order of tasks (by ID): ", [job[0] for job in optimum_order])
print("Time spent on tasks: ", cmax)