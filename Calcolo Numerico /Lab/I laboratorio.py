import matplotlib.pyplot as plt
import numpy as np

#ESERCIZIO 1:
import sys
help(sys.float_info)
print(sys.float_info)
#understand the meaning of:
# 1. max: maximum representable finite float 
# 2. max exp: maximum int e such that radix**(e-1) is representable
# 3. max 10 exp: maximum int e such that 10**e is representable


#Inizializzazione delle variabili per il calcolo della precisione macchina
nmax = 100 #numero massimo di iterazioni
n = 0
eps = 1
floateps = eps + 1 #definizione fl(eps + 1) > 1

while floateps > 1 and n < nmax:
    n = n+1
    eps = eps/2
    floateps = eps + 1
    
eps = 2 * eps #ultimo valore tale per cui vale ancora il while

#Calcola il numero di cifre della mantissa
mantissa_digits = sys.float_info.mant_dig

print("Epsylon =", eps)
print("Numero di cifre della mantissa:", mantissa_digits)


#Utilizzo NumPy per esplorare le differenze tra float16 e float32
#e verifica il risultato di np.finfo(float).eps

#Calcola la precisione macchina per float16
eps_float16 = 1.0

while np.float16(1.0) + np.float16(eps_float16) > np.float16(1.0):
    eps_float16 /= 2.0

#Calcola la precisione macchina per float32
eps_float32 = 1.0

while np.float32(1.0) + np.float32(eps_float32) > np.float32(1.0):
    eps_float32 /= 2.0

#Verifica il risultato di np.finfo(float).eps
eps_numpy_float = np.finfo(float).eps

print(f"\nPrecisione macchina per float16:", eps_float16)
print(f"Precisione macchina per float32:", eps_float32)
print(f"Precisione float di NumPy:", eps_numpy_float)



#ESERCIZIO 2: plot of a function
#2.1
x = np.linspace(0, 10)

y1 = np.sin(x)
y2 = np.cos(x)

plt.plot(x, y1, "--m*")
plt.plot(x, y2, "--b*")

plt.xlabel("x")
plt.ylabel("y")

plt.legend(["sin(x)", "cos(x)"], loc = "upper right")
plt.title("$\sin(x)$, $\cos(x)$")

plt.show() 


#2.2
def fib(n):
    if n == 0 or n == 1:
        return n
        
    else:
        return fib(n-1) + fib(n-2)
    
def golden_ratio(k):
    if k>0: #per definizione
        return fib(k+1)/fib(k)
    
x = np.arange(1,20)
y = [golden_ratio(k) for k in x] #vettore di tutti i rapporti

sigma = (1+np.sqrt(5))/2 #sezione aurea

plt.plot(x,y) #plot dei rapporti al variare di x
plt.plot(x, sigma*np.ones(np.shape(x))) #plot della retta di sezione aurea

plt.legend(["ratio", r"$\phi$"])
plt.show()        
        
z = np.abs(y - sigma*np.ones(np.shape(x))) #errore; distanza tra le due funzioni

plt.plot(x,z) #plot dell'errore 
