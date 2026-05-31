import math
import copy

def tabue_search(n, it_limit, cadance):
    pi = init_solution()

    pi_star = copy.deepcopy(pi)

    tabu_list = { (j, k): 0 for j in range(1, n+1) for k in range(1, n+1) }

    for it in range(1, it_limit + 1):
        c_best = math.inf
        j_star, k_star = None, None

        for j in range(1, n + 1):
            for k in range(j + 1, n + 1):
                if tabu_list.get((j, k), 0) < it:
                    pi_new = move(pi, j, k)
                    cost_new = calculate(pi_new)
                    if cost_new < c_best:
                        c_best = cost_new

                        j_star = j
                        k_star = k
    
    if j_star is not None and k_star is not None:
        pi = move(pi, j_star, k_star)

        tabu_list[(j_star, k_star)] = it + cadance
        tabu_list[(j_star, k_star)] = it + cadance

        if calculate(pi) < calculate(pi_star):
            pi_star = copy.deepcopy(pi)
    
    return pi_star

def init_solution():
    # Inicjalizacja rozwiązania początkowego (np. losowe permutacje)
    pass

def calculate(solution):
    # Obliczanie wartości funkcji celu dla danego rozwiązania pi
    pass

def move(solution, j, k):
    new_solution = copy.deepcopy(solution)
    return new_solution
