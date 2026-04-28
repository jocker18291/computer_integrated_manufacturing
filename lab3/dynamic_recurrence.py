def dp_total_weighted_tardiness(p, w, d):
    n = len(p)
    max_mask = 1 << n

    memory = [float('inf')] * max_mask
    memory[0] = 0

    for mask in range(1, max_mask):
        sum_p = 0
        for j in range(n):
            if mask & (1 << j):
                sum_p += p[j]
        
        for j in range(n):
            if mask & (1 << j):
                tardiness = max(sum_p - d[j], 0)
                cost = tardiness * w[j]

                prev_mask = mask ^ (1 << j)

                total_cost = cost + memory[prev_mask]

                if total_cost < memory[mask]:
                    memory[mask] = total_cost
    
    return memory[max_mask - 1]

