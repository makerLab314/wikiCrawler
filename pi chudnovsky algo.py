import math
from decimal import ROUND_FLOOR, Decimal, getcontext


iterations = 10000
getcontext().prec = int(iterations * 1.205) + 20
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

answ = r / Decimal(2)
nb = answ**2
nb = (Decimal(1) - nb).sqrt()
nb = Decimal(2) * nb
sn = (Decimal(2) - nb).sqrt()
seiten = seiten * Decimal(2)


for i in range(iterations):
    seiten = seiten * Decimal(2)
    answ = sn / Decimal(2)
    nb = answ**2
    nb = (Decimal(1) - nb).sqrt()
    nb = Decimal(2) * nb
    sn = (Decimal(2) - nb).sqrt()
    tot_iterations_debug = seiten
    pi = sn * tot_iterations_debug / Decimal(2)
    finale_abweichung = abs(control_pi_decimal - pi)
    # korrekte_stellen = -int(finale_abweichung.log10().to_integral_value(rounding=ROUND_FLOOR))
    
    # Eine schöne Ausgabe für jede Iteration:
    # print(f"Zwischenergebis: {korrekte_stellen} korrekte Stellen")
    print("-" * 30)
    print(f"Iteration {i + 1}:")
 

pi = sn * tot_iterations
print("\nFINAL RESULT: ", pi)
finale_abweichung = abs(control_pi_decimal - pi)
korrekte_stellen = -int(finale_abweichung.log10().to_integral_value(rounding=ROUND_FLOOR))
print("Korrekte Stellen:", korrekte_stellen)