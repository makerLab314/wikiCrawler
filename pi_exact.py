from decimal import Decimal, getcontext

# Wir zwingen Python, mit 1000 Nachkommastellen Genauigkeit zu rechnen
getcontext().prec = 1000 

iterations = 35

# Alle Startwerte müssen zu "Decimal" gemacht werden, sonst nutzt Python wieder normale Floats
r = Decimal('1') 
sn = Decimal('0')
pi = Decimal('0')
tot_iterations = iterations + 1

answ = r / 2
nb = answ**2
nb = (Decimal('1') - nb).sqrt()
nb = 2 * nb
sn = (Decimal('2') - nb).sqrt()

for i in range(iterations):
    answ = sn / 2
    nb = answ**2
    nb = (Decimal('1') - nb).sqrt()
    nb = 2 * nb
    sn = (Decimal('2') - nb).sqrt()

tot_iterations = 3 * (2 ** tot_iterations)

# Da tot_iterations ein int ist und sn ein Decimal, kann Python das jetzt multiplizieren!
pi = sn * tot_iterations
print(pi)