import math
import copy
import random
from utils import oblicz_cmax

def random_search(jobs_list, test_data, iterations=1000):
    best_solution = None
    best_cmax = math.inf

    for _ in range(iterations):
        current_solution = copy.deepcopy(jobs_list)
        random.shuffle(current_solution)
        current_cmax = oblicz_cmax(current_solution, test_data)

        if current_cmax < best_cmax:
            best_cmax = current_cmax
            best_solution = current_solution
    
    return best_solution, best_cmax