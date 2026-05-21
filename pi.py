import math
from decimal import Decimal, getcontext


iterations = 200
r = Decimal(1)
sn = 0
pi = 0
answ = 0
nb = 0
tot_iterations = iterations + 1
tot_iterations = 3 * (2 ** tot_iterations)
seiten = Decimal(6)
getcontext().prec = 300
control_pi = Decimal("3.141592653589793238462643383279502884197169399375105820974944592307816406286208998628034825342117067982148086513282306647093844609550582231725359408128481117450284102701938521105559644622948954930381964428810975665933446128475648233786783165271201909145648566923460348610454326648213393607260249141273")


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

    abweichung = abs(control_pi - pi)
    
    # Eine schöne Ausgabe für jede Iteration:
    print(f"--- Iteration {i+1} ---")
    print(f"Berechnet:  {pi}")
    print(f"Abweichung: {abweichung}")
    print("-" * 30)

    print(pi)

 

pi = sn * tot_iterations
print("\nFINAL RESULT: ", pi)
finale_abweichung = abs(control_pi - pi)
print("FINALE ABWEICHUNG:", finale_abweichung)