import copy

from utils import oblicz_cmax


def _init_solution(dane_zadan):
    """Rozwiazanie poczatkowe: permutacja naturalna (rosnace ID zadan)."""
    return sorted(dane_zadan.keys())


def _move(permutacja, i, j):
    """Ruch SWAP: zamiana zadan na pozycjach i oraz j."""
    nowa = permutacja.copy()
    nowa[i], nowa[j] = nowa[j], nowa[i]
    return nowa


def _para_klucz(i, j):
    return (i, j) if i < j else (j, i)


def przeszukiwanie_z_zabronieniami(dane_zadan, it_limit=100, kadencja=7):
    """
    Implementacja algorytmu Przeszukiwania z Zabronieniami (Tabu Search)

    Sasiadztwo: zamiana par zadan (swap). Lista tabu przechowuje ruchy
    zabronione do iteracji it + kadencja. Dopuszczalne jest przełamanie
    listy tabu (aspiracja), gdy nowe rozwiazanie poprawia najlepsze dotychczas.
    """
    n = len(dane_zadan)
    pi = _init_solution(dane_zadan)

    pi_najlepsze = copy.deepcopy(pi)
    cmax_najlepsze = oblicz_cmax(pi, dane_zadan)

    tabu_list = {}

    for it in range(1, it_limit + 1):
        c_best = float("inf")
        i_star = j_star = None
        pi_najlepszy_ruch = None

        for i in range(n):
            for j in range(i + 1, n):
                para = _para_klucz(i, j)
                is_tabu = tabu_list.get(para, 0) >= it

                pi_nowe = _move(pi, i, j)
                koszt_nowy = oblicz_cmax(pi_nowe, dane_zadan)

                # Aspiracja: przełamanie tabu, gdy poprawiamy globalne optimum
                if is_tabu and koszt_nowy >= cmax_najlepsze:
                    continue

                if koszt_nowy < c_best:
                    c_best = koszt_nowy
                    i_star = i
                    j_star = j
                    pi_najlepszy_ruch = pi_nowe

        if i_star is None:
            break

        pi = pi_najlepszy_ruch
        tabu_list[_para_klucz(i_star, j_star)] = it + kadencja

        if c_best < cmax_najlepsze:
            pi_najlepsze = copy.deepcopy(pi)
            cmax_najlepsze = c_best

    return pi_najlepsze, cmax_najlepsze
