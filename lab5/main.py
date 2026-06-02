import random
import sys
from pathlib import Path

from random_search import random_search
from simulated_annealing import symulowane_wyzarzanie
from tabue_search import przeszukiwanie_z_zabronieniami
from utils import DANE_TESTOWE, oblicz_cmax

ROOT = Path(__file__).resolve().parents[1]
LAB4 = ROOT / "lab4"
if str(LAB4) not in sys.path:
    sys.path.insert(0, str(LAB4))

from neh import neh


def _neh_dla_slownika(dane_zadan):
    klucze = sorted(dane_zadan.keys())
    macierz_p = [dane_zadan[k] for k in klucze]
    kolejnosc_idx, cmax = neh(macierz_p)
    kolejnosc = [klucze[i] for i in kolejnosc_idx]
    return kolejnosc, cmax


if __name__ == "__main__":

    # Wyświetlanie definiowanego problemu (DANE_TESTOWE)
    print("\n==================================================")
    print("               DANE PROBLEMU (FLOW SHOP)          ")
    print("==================================================")
    print(" Zadanie | M1 | M2 | M3 ")
    print("------------------------")
    for zadanie, czasy in DANE_TESTOWE.items():
        # Zakładając, że maszyny to kolejne elementy listy
        czasy_str = " | ".join(f"{czas:2}" for czas in czasy)
        print(f"    {zadanie:2}   | {czasy_str} ")
    print("==================================================\n")

    permutacja_poczatkowa = list(DANE_TESTOWE.keys())
    random.shuffle(permutacja_poczatkowa)
    cmax_poczatkowe = oblicz_cmax(permutacja_poczatkowa, DANE_TESTOWE)

    print("[STAN POCZĄTKOWY]")
    print(f"Losowa sekwencja zadań (permutacja początkowa): {permutacja_poczatkowa}")
    print(f"C_max początkowe:                               {cmax_poczatkowe}")

    T0 = 100.0
    T_END = 0.01
    L = 20
    ALPHA = 0.95

    najlepsza_sekwencja_sa, najlepsze_cmax_sa = symulowane_wyzarzanie(
        T0, T_END, L, ALPHA, DANE_TESTOWE
    )

    najlepsza_sekwencja_tabu, najlepsze_cmax_tabu = przeszukiwanie_z_zabronieniami(
        DANE_TESTOWE, it_limit=100, kadencja=7
    )

    najlepsza_sekwencja_3, najlepsze_cmax_3 = random_search(
        permutacja_poczatkowa, DANE_TESTOWE, iterations=1000
    )

    kolejnosc_neh, cmax_neh = _neh_dla_slownika(DANE_TESTOWE)

    print("\n==================================================")
    print("               PORÓWNANIE WYNIKÓW                 ")
    print("==================================================")
    print(f"1. Rozwiązanie losowe:            C_max = {cmax_poczatkowe}")
    print(
        f"2. Random Search:                 C_max = {najlepsze_cmax_3}"
        f" | sekwencja: {najlepsza_sekwencja_3}"
    )
    print(
        f"3. NEH (lab4, konstrukcyjny):     C_max = {cmax_neh}"
        f" | sekwencja: {kolejnosc_neh}"
    )
    print(
        f"4. Symulowane Wyzarzanie:         C_max = {najlepsze_cmax_sa}"
        f" | sekwencja: {najlepsza_sekwencja_sa}"
    )
    print(
        f"5. Tabu Search:                   C_max = {najlepsze_cmax_tabu}"
        f" | sekwencja: {najlepsza_sekwencja_tabu}"
    )
    print("==================================================")

    zysk_sa = cmax_poczatkowe - najlepsze_cmax_sa
    zysk_tabu = cmax_poczatkowe - najlepsze_cmax_tabu
    print(f"SA skrócił C_max o:   {zysk_sa}")
    print(f"Tabu skrócił C_max o: {zysk_tabu}")