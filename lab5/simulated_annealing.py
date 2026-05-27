import math
import random
from utils import oblicz_cmax


def symulowane_wyzarzanie(t0, t_end, L, alpha, dane_zadan):
    """Implementacja algorytmu Symulowanego Wyżarzania na ocenę 4.0."""
    zadania = list(dane_zadan.keys())

    # Rozwiązanie początkowe
    pi_aktualne = zadania.copy()
    random.shuffle(pi_aktualne)
    cmax_aktualne = oblicz_cmax(pi_aktualne, dane_zadan)

    pi_najlepsze = pi_aktualne.copy()
    cmax_najlepsze = cmax_aktualne

    t = t0

    while t > t_end:
        for k in range(L):
            # Ruch SWAP
            n = len(pi_aktualne)
            i = random.randint(0, n - 1)
            j = random.randint(0, n - 1)
            while i == j:
                j = random.randint(0, n - 1)

            pi_nowe = pi_aktualne.copy()
            pi_nowe[i], pi_nowe[j] = pi_nowe[j], pi_nowe[i]

            cmax_nowe = oblicz_cmax(pi_nowe, dane_zadan)
            delta = cmax_aktualne - cmax_nowe

            # Kryterium akceptacji Metropolis
            if delta >= 0:
                pi_aktualne = pi_nowe.copy()
                cmax_aktualne = cmax_nowe
            else:
                p = math.exp(delta / t)
                if random.random() < p:
                    pi_aktualne = pi_nowe.copy()
                    cmax_aktualne = cmax_nowe

            if cmax_aktualne < cmax_najlepsze:
                pi_najlepsze = pi_aktualne.copy()
                cmax_najlepsze = cmax_aktualne

        t = alpha * t

    return pi_najlepsze, cmax_najlepsze