import math
from decimal import ROUND_DOWN, ROUND_FLOOR, Decimal, getcontext
import time
from tqdm import tqdm
import gmpy2

start_zeit = time.perf_counter()


iterations = 10000

gmpy2.get_context().precision = int((int(iterations * 1.205) + 20) * 3.322) + 1

r = gmpy2.mpfr(1)
sn = gmpy2.mpfr(0)
pi = gmpy2.mpfr(0)
answ = gmpy2.mpfr(0)
nb = gmpy2.mpfr(0)
tot_iterations = iterations + 1
tot_iterations = 3 * (2 ** tot_iterations)
seiten = gmpy2.mpfr(6)

with open("pi_reference.txt.txt", "r", encoding="utf-8") as file:
    # Read the whole file content into the variable
    control_pi = file.read()

control_pi_decimal = gmpy2.mpfr(control_pi.strip())

answ = r / gmpy2.mpfr(2)
nb = answ**2
nb = gmpy2.sqrt(gmpy2.mpfr(1) - nb)
nb = gmpy2.mpfr(2) * nb
sn = gmpy2.sqrt(gmpy2.mpfr(2) - nb)
seiten = seiten * gmpy2.mpfr(2)

loop = tqdm(range(iterations), desc="Calculating Pi", unit="iter")



for i in loop:
    zwei = gmpy2.mpfr(2)
    vier = gmpy2.mpfr(4)
    seiten = seiten * zwei
    answ = sn / zwei
    nb = answ**2
    nb = gmpy2.sqrt(gmpy2.mpfr(1) - nb)
    nb = zwei * nb
    sn = gmpy2.sqrt(zwei - nb)
    tot_iterations_debug = seiten
    pi = sn * tot_iterations_debug / gmpy2.mpfr(2)
    # finale_abweichung = abs(control_pi_decimal - pi)
    # korrekte_stellen = -int(finale_abweichung.log10().to_integral_value(rounding=ROUND_FLOOR))
    
    # Eine schöne Ausgabe für jede Iteration:
    # print(f"Zwischenergebis: {korrekte_stellen} korrekte Stellen")
    # print("-" * 30)
    # print(f"Iteration {i + 1}:")
 

pi = sn * tot_iterations
print("\nFINAL RAW RESULT: ", pi)

finale_abweichung = abs(control_pi_decimal - pi)
korrekte_stellen = -int(gmpy2.log10(finale_abweichung))
if finale_abweichung > 0:
    korrekte_stellen = -int(gmpy2.log10(finale_abweichung))
else:
    korrekte_stellen = int(gmpy2.get_context().precision / 3.32193)

pi_as_string = f"{pi:.{korrekte_stellen + 5}f}"

vorkomma, nachkomma = pi_as_string.split(".")
nachkomma_abgeschnitten = nachkomma[:korrekte_stellen]

pi_korr = f"{vorkomma}.{nachkomma_abgeschnitten}"



print("Korrekte Stellen:", korrekte_stellen)
print("Korrigiertes Ergebnis:", pi_korr)
end_zeit = time.perf_counter()
print(f"Berechnungszeit: {end_zeit - start_zeit:.2f} Sekunden")

