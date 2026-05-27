def oblicz_cmax(permutacja, dane_zadan):
    liczba_maszyn = len(dane_zadan[permutacja[0]])
    c = [0] * liczba_maszyn

    for zadanie in permutacja:
        czasy_maszyn = dane_zadan[zadanie]
        c[0] += czasy_maszyn[0]
        for j in range(1, liczba_maszyn):
            c[j] = max(c[j], c[j - 1]) + czasy_maszyn[j]

    return c[-1]

DANE_TESTOWE = {
    1: [4, 3, 5],
    2: [2, 6, 2],
    3: [5, 1, 4],
    4: [3, 4, 3],
    5: [6, 2, 5],
}