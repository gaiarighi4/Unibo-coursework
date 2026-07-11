" 2. Risoluzione di sistemi lineari con fattorizzazione di Cholesky (Matrice tridiagonale)"

import numpy as np
import scipy
import scipy.linalg

# Creazione dati e problema test
n = 4 # dimensione della matrice
A = np.eye(n)*9 - np.eye(n, k = -1)*4 - np.eye(n, k = 1)*4 
x = np.ones((n, 1))
b = A@x 

print("\nA.shape: ", A.shape)
print("x.shape: ", x.shape)
print("b.shape: ", b.shape)

# Numero di condizione
condA = np.linalg.cond(A, 2)
print("\nK(A) = ", condA)

# Fattorizzazione di Cholesky
L = scipy.linalg.cholesky(A, lower = True) # lower=True indica che si vuole ottenere la matrice triangolare inferiore L

print('\nL:', L) # stampa la matrice triangolare inferiore L ottenuta dalla fattorizzazione di Cholesky di A
print('\nL*L.T =', np.matmul(L, np.transpose(L))) # stampa L * L.T, che dovrebbe approssimarsi alla matrice A
print('\nErrore fattorizzazione Cholesky = ', scipy.linalg.norm(A-np.matmul(L, np.transpose(L)), 'fro')) # calcola l'errore tra la matrice A e il suo approssimato ottenuto da L * L.T

y = scipy.linalg.solve_triangular(L, b, lower = True) # risolve L * y = b. La funzione solve_triangular viene utilizzata per risolvere sistemi lineari con matrici triangolari
my_x = scipy.linalg.solve(np.transpose(L), y, lower = False) # risolve L.T * my_x = y 

print('\nmy_x = ', my_x) 
print("\nNorma dell'errore = ", np.linalg.norm(x-my_x, 'fro')) # calcola e stampa la norma dell'errore tra la soluzione esatta x e la soluzione calcolata my_x

