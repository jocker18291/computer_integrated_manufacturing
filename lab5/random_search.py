import math
import copy
import random
from utils import oblicz_cmax

def random_search(jobs, iterations=1000):
    best_solution = None
    best_cmax = math.inf

    for _ in range(iterations):
        current_solution = copy.deepcopy(jobs)
        random.shuffle(current_solution)
        current_cmax = oblicz_cmax(current_solution)

        if current_cmax < best_cmax:
            best_cmax = current_cmax
            best_solution = current_solution
    
    return best_solution, best_cmax