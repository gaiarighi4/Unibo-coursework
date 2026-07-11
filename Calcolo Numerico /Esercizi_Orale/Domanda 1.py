" 1. Risoluzione di sistemi lineari con fattorizzazione LU con pivoting "

import numpy as np
import random
import scipy.linalg

# Creazione dati e problema test
n = random.randint(10, 1000) # utilizza la funzione randint del modulo random per generare un numero intero casuale tra 10 e 999
A = np.random.randn(n, n) # matrice a valori randomici tra 10 e 999
x = np.ones((n, 1)) # soluzione esatta; crea un vettore di tutti 1
b = A@x # prodotto matrice per vettore

print("\nA.shape: ", A.shape)
print("x.shape: ", x.shape)
print("b.shape: ", b.shape)

# Numero di condizione
condA = np.linalg.cond(A, 2)
print("\nK(A) = ", condA)

# Fattorizzazione LU con pivoting
lu, piv = scipy.linalg.lu_factor(A) # calcola la decomposizione LU di A e restituisce due oggetti:
    # lu: matrice decomposta LU
    # piv: pivot utilizzati durante la fattorizzazione

print('\nlu = ', lu,) # stampa la matrice lu, che contiene sia la parte lower-triangular (L) che la parte upper-triangular (U) della decomposizione
print('\npiv =', piv,) # stampa il vettore piv (utilizzati per mantenere la stabilità numerica della fattorizzazione)

# Risoluzione di    Ax = b   <--->  PLUx = b 
my_x = scipy.linalg.lu_solve((lu, piv), b) # risolve il sistema lineare Ax = b utilizzando la decomposizione LU precedentemente calcolata

print("\nmy_x = ", my_x) # stampa la soluzione del sistema lineare ottenuta utilizzando la decomposizione LU
print("\nNorma dell'errore = ", np.linalg.norm(x-my_x, 'fro')) # calcola e stampa la norma dell'errore tra la soluzione esatta x e la soluzione calcolata my_x


