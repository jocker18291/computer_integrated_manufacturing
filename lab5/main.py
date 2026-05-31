import random
from simulated_annealing import symulowane_wyzarzanie
from utils import DANE_TESTOWE, oblicz_cmax
from random_search import random_search

if __name__ == "__main__":

    permutacja_poczatkowa = list(DANE_TESTOWE.keys())
    random.shuffle(permutacja_poczatkowa)
    cmax_poczatkowe = oblicz_cmax(permutacja_poczatkowa, DANE_TESTOWE)

    print("\n[STAN POCZĄTKOWY]")
    print(f"Losowa sekwencja zadań: {permutacja_poczatkowa}")
    print(f"C_max początkowe:       {cmax_poczatkowe}")

    T0 = 100.0
    T_END = 0.01
    L = 20
    ALPHA = 0.95

    najlepsza_sekwencja_4, najlepsze_cmax_4 = symulowane_wyzarzanie(
        T0, T_END, L, ALPHA, DANE_TESTOWE
    )

    print("\n==================================================")
    print("               PORÓWNANIE WYNIKÓW                 ")
    print("==================================================")
    print(
        f"1. Rozwiązanie Losowe:       C_max = {cmax_poczatkowe} (Odniesienie)"
    )
    najlepsza_sekwencja_3, najlepsze_cmax_3 = random_search(permutacja_poczatkowa, DANE_TESTOWE, iterations=1000)
    print(
        f"2. Local/Random Search (3.0): C_max = {najlepsze_cmax_3} | Najlepsza sekwencja: {najlepsza_sekwencja_3}"
    )

    print(
        f"3. Symulowane Wyżarzanie (4.0): C_max = {najlepsze_cmax_4} | Najlepsza sekwencja: {najlepsza_sekwencja_4}"
    )

    # print(f"4. Algorytm dla J||Cmax (5.0): C_max = {cmax_5_0}")
    print("==================================================")

    zysk = cmax_poczatkowe - najlepsze_cmax_4
    print(
        f"Algorytm symulowanego wyzarzania skrócił c_max o: {zysk}"
    )