" 3. Risoluzione di sistemi lineari con fattorizzazione di Cholesky (Matrice di Hilbert"

import numpy as np
import scipy.linalg
import random

# Creazione dati e problema test
n = random.randint(2, 16)
A = scipy.linalg.hilbert(n)
x = np.ones((n, 1)) 
b = A@x

print("\nA.shape", A.shape) # stampa la dimensione
print("x.shape", x.shape)
print("b.shape", b.shape)

# Numero di condizione
condA = np.linalg.cond(A, 2)
print("\nK(A) = ", condA)

# Fattorizzazione di Cholesky
L = scipy.linalg.cholesky(A, lower = True) 

print('\nL:', L)
print('\nL*L.T =', np.matmul(L, np.transpose(L))) 
print('\nErrore fattorizzazione Cholesky = ', scipy.linalg.norm(A-np.matmul(L, np.transpose(L)), 'fro')) 

y = scipy.linalg.solve(L, b, lower = True) 
my_x = scipy.linalg.solve(np.transpose(L), y, lower = False) 

print('\nmy_x = ', my_x)
print("\nNorma dell'errore = ", np.linalg.norm(x-my_x, 'fro'))  # calcola e stampa la norma dell'errore tra la soluzione esatta x e la soluzione calcolata my_x




