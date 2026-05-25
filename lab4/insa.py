from collections import deque

def evaluate_makespan(machine_seqs, jobs_data):
    """
    Oblicza C_max dla częściowego harmonogramu przy użyciu metody ścieżki krytycznej.
    Zwraca float('inf') jeśli wygenerowany graf zawiera cykle.
    """
    in_degree = {}
    adj = {}
    proc_time = {}
    
    # Inicjalizacja wierzchołków grafu.
    # Węzłem w grafie jest krotka (id_zadania, indeks_operacji)
    for seq in machine_seqs.values():
        for op in seq:
            in_degree[op] = 0
            adj[op] = []
            
    # Budowanie krawędzi grafu disjunktywnego
    for seq in machine_seqs.values():
        for i, (job_id, op_idx) in enumerate(seq):
            proc_time[(job_id, op_idx)] = jobs_data[job_id][op_idx][1]
            
            # Krawędzie koniunktywne (wynikające z kolejności technologicznej wewnątrz zadania)
            if op_idx > 0:
                prev_op = (job_id, op_idx - 1)
                # poprzednia operacja musi być w grafie, gdyż wstawiamy je po kolei
                if prev_op in adj:
                    adj[prev_op].append((job_id, op_idx))
                    in_degree[(job_id, op_idx)] += 1
            
            # Krawędzie disjunktywne (wynikające z ustalonej kolejności na maszynie)
            if i < len(seq) - 1:
                next_op = seq[i+1]
                adj[(job_id, op_idx)].append(next_op)
                in_degree[next_op] += 1
                
    # Sortowanie topologiczne (Algorytm Kahna) do wyznaczenia najdłuższej ścieżki
    queue = deque([u for u, deg in in_degree.items() if deg == 0])
    visited_count = 0
    est = {u: 0 for u in in_degree} # Earliest Start Time
    
    while queue:
        u = queue.popleft()
        visited_count += 1
        for v in adj[u]:
            in_degree[v] -= 1
            # Relaksacja najdłuższej ścieżki
            est[v] = max(est[v], est[u] + proc_time[u])
            if in_degree[v] == 0:
                queue.append(v)
                
    # Wykrycie cyklu (jeśli nie odwiedziliśmy wszystkich wierzchołków w DAG)
    if visited_count < len(in_degree):
        return float('inf')
        
    # C_max to maksimum z sumy czasu rozpoczęcia i czasu trwania operacji dla wszystkich węzłów
    makespan = max((est[u] + proc_time[u] for u in est), default=0)
    return makespan

def INSA(jobs_data):
    """
    Algorytm INSA (Insertion Algorithm) dla problemu J||C_max.
    
    :param jobs_data: Lista zadań. Każde zadanie to lista operacji.
                      Operacja to krotka: (id_maszyny, czas_wykonania).
    :return: (makespan, harmonogram)
    """
    num_jobs = len(jobs_data)
    
    # Krok 1: Oblicz całkowity czas wykonania poszczególnych zadań
    job_totals = [sum(time for m, time in job) for job in jobs_data]
    
    # Sortuj zadania nierosnąco na podstawie całkowitego czasu
    order = sorted(range(num_jobs), key=lambda x: job_totals[x], reverse=True)
    
    # Identyfikacja wykorzystywanych maszyn
    machines = set()
    for job in jobs_data:
        for m, time in job:
            machines.add(m)
            
    # Zbiór sekwencji operacji dla poszczególnych maszyn
    machine_seqs = {m: [] for m in machines}
    
    # Krok 2: Faza konstrukcyjna
    for job_id in order:
        job = jobs_data[job_id]
        
        # Wstawiamy operacje po kolei dla analizowanego zadania
        for op_idx, (m, time) in enumerate(job):
            best_makespan = float('inf')
            best_pos = -1
            
            seq = machine_seqs[m]
            
            # Próbujemy wstawić nową operację na wszystkie możliwe pozycje w sekwencji przypisanej do maszyny
            for pos in range(len(seq) + 1):
                seq.insert(pos, (job_id, op_idx))
                
                # Ocena C_max aktualnego wariantu częściowego
                makespan = evaluate_makespan(machine_seqs, jobs_data)
                
                if makespan < best_makespan:
                    best_makespan = makespan
                    best_pos = pos
                    
                # Wycofanie zmiany, by sprawdzić następną pozycję
                seq.pop(pos)
                
            if best_pos != -1:
                # Trwałe wstawienie operacji na najlepszą znalezioną, acykliczną pozycję
                seq.insert(best_pos, (job_id, op_idx))
            else:
                raise ValueError(f"Nie znaleziono acyklicznej pozycji dla operacji {(job_id, op_idx)} na maszynie {m}. Problem może być niespójny.")
                
    final_makespan = evaluate_makespan(machine_seqs, jobs_data)
    return final_makespan, machine_seqs
