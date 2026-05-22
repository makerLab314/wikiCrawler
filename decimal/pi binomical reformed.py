import math
from decimal import ROUND_DOWN, ROUND_FLOOR, Decimal, getcontext
import time
from tqdm import tqdm

start_zeit = time.perf_counter()


iterations = 10000
getcontext().prec = int(iterations * 0.602) + 10
r = Decimal(1)
sn = 0
pi = 0
answ = 0
nb = 0
tot_iterations = iterations + 1
tot_iterations = 3 * (2 ** tot_iterations)
seiten = Decimal(6)

with open("pi_reference.txt.txt", "r", encoding="utf-8") as file:
    # Read the whole file content into the variable
    control_pi = file.read()

control_pi_decimal = Decimal(control_pi.strip())



answ = Decimal(4) - r**2
nb = Decimal(2) + answ.sqrt()
nb = nb.sqrt()
sn = Decimal(r) / nb
seiten = seiten * Decimal(2)

loop = tqdm(range(iterations), desc="Calculating Pi", unit="iter")



for i in loop:
    seiten = seiten * Decimal(2)
    answ = Decimal(4) - sn**2
    nb = Decimal(2) + answ.sqrt()
    nb = nb.sqrt()
    sn = Decimal(sn) / nb
    tot_iterations_debug = seiten
    pi = sn * tot_iterations_debug / Decimal(2)
    # finale_abweichung = abs(control_pi_decimal - pi)
    # korrekte_stellen = -int(finale_abweichung.log10().to_integral_value(rounding=ROUND_FLOOR))
    
    # Eine schöne Ausgabe für jede Iteration:
    # print(f"Zwischenergebis: {korrekte_stellen} korrekte Stellen")
    # print("-" * 30)
    # print(f"Iteration {i + 1}:")
 

pi = sn * tot_iterations
print("\nFINAL RAW RESULT: ", pi)

finale_abweichung = abs(control_pi_decimal - pi)
korrekte_stellen = -int(finale_abweichung.log10().to_integral_value(rounding=ROUND_FLOOR))
maske = Decimal('10') ** -korrekte_stellen
pi_korr = pi.quantize(maske, rounding=ROUND_DOWN)
print("Korrekte Stellen:", korrekte_stellen)
print("Korrigiertes Ergebnis:", pi_korr)
end_zeit = time.perf_counter()
print(f"Berechnungszeit: {end_zeit - start_zeit:.2f} Sekunden")

