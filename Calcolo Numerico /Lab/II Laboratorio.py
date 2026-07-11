"""1. matrici e norme """
import numpy as np

#help(np.linalg) # View source
#help (np.linalg.norm)
#help (np.linalg.cond)

n = 2
A = np.array([[1, 2], [0.499, 1.001]])

print ('Norme di A:')

norm1 = np.linalg.norm(A, 1)
norm2 = np.linalg.norm(A, 2)
normfro = np.linalg.norm(A, "fro")
norminf = np.linalg.norm(A, np.inf)

print('Norma 1 = ', norm1, '\n')
print('Norma 2 = ', norm2, '\n')
print('Norma Frobenius = ', normfro, '\n')
print('Norma infinito = ', norminf, '\n')

cond1 = np.linalg.cond(A, 1)
cond2 = np.linalg.cond(A, 2)
condfro = np.linalg.cond(A, "fro")
condinf = np.linalg.cond(A, np.inf)

print ('K(A)_1 = ', cond1, '\n')
print ('K(A)_2 = ', cond2, '\n')
print ('K(A)_Frobenius =', condfro, '\n')
print ('K(A)_infinito =', condinf, '\n')

x = np.ones((2,1))
b = np.dot(A,x) 

btilde = np.array([[3], [1.4985]])
xtilde = np.array([[2, 0.5]]).T

# Verificare che xtilde è soluzione di A xtilde = btilde (Axtilde)
my_btilde = np.dot(A,xtilde)

print ('A*xtilde = ', btilde)
print(np.linalg.norm(btilde-my_btilde,'fro'))

deltax = np.linalg.norm(x - xtilde, 2) 
deltab = np.linalg.norm(b - btilde, 2) 

print ('delta x = ', deltax) #condizionamento orribile
print ('delta b = ', deltab) #idem




"""2. fattorizzazione lu"""

import numpy as np
import builtins 

#Creazione dati e problema test
A = np.array ([ [3,-1, 1,-2], [0, 2, 5, -1], [1, 0, -7, 1], [0, 2, 1, 1]  ])
x = np.ones((4,1)) #soluzione esatta; crea una atrice di tutti 1, con 4 righe e una colonna
b = A @ x #come si scrive il termine noto; prodotto matrice per vettore 

condA = np.linalg.cond(A)
n=A.shape[0] #mi dà il numero di righe
print('x: \n', x , '\n')
print('x.shape: ', x.shape, '\n' )
print('b: \n', b , '\n')
print('b.shape: ', b.shape, '\n' )
print('A: \n', A, '\n')
print('A.shape: ', A.shape, '\n' )
print('K(A)=', condA, '\n')

import scipy
# help (scipy)
import scipy.linalg
# help (scipy.linalg)
import scipy.linalg.decomp_lu as LUdec 
#from scipy.linalg import lu_factor as LUdec # pivoting
#from scipy.linalg import lu_factor as LUfull # partial pivoting

lu, piv = scipy.linalg.lu_factor(A)

print('lu',lu,'\n')
print('piv',piv,'\n')


# risoluzione di    Ax = b   <--->  PLUx = b 
my_x = scipy.linalg.lu_solve((lu, piv), b) #come trova la soluzione della fattorizzazione

print('my_x = \n', my_x)
print('norm =', scipy.linalg.norm(x-my_x, 'fro'))

# IMPLEMENTAZIONE ALTERNATIVA - 1

L, U = np.tril(lu, k = -1) + np.eye(n), np.triu(lu)  #scompone LU in L matrice triangolare inferiore, U matrice triangolare superiore
P = np.eye(n)[piv]

print ('A = ', A)
print ('P = ', P)
print ('L = ', L)
print ('U = ', U)
print ('P*L*U = ', np.matmul(P , np.matmul(L, U))) 

print ('diff = ',   np.linalg.norm(A - np.matmul(P , np.matmul(L, U)), 'fro'  ) ) 


if np.all(P != np.eye(n)): 
# Ax = b   <--->  PLUx = b  <--->  LUx = inv(P)b  <--->  Ly=inv(P)b & Ux=y : matrici triangolari
# quindi
     invP = np.linalg.inv(P)
     y = scipy.linalg.solve_triangular(L,invP@b, lower=True, unit_diagonal=True)
     my_x = scipy.linalg.solve_triangular(U,y, lower=False)

if np.all(P == np.eye(n)): 
#Ax = b   <--->  PLUx = b  <--->  PLy=b & Ux=y
     y = scipy.linalg.solve_triangular(np.matmul(P,L) , b, lower=True, unit_diagonal=True)
     my_x = scipy.linalg.solve_triangular(U, y, lower=False)

print('\nSoluzione calcolata: ', my_x)
print('norm =', scipy.linalg.norm(x-my_x, 'fro'))

input()

"""2.2 Choleski con matrice di Hilbert"""
import matplotlib.pyplot as plt
import numpy as np
import scipy
# help (scipy)
import scipy.linalg
# help (scipy.linalg)
# help (scipy.linalg.cholesky)
# help (scipy.linalg.hilbert)

# crazione dati e problema test
n = 5
A = scipy.linalg.hilbert(n)
x = np.ones((n, 1))
b = A @ x

condA = np.linalg.cond(A)


print('x: \n', x , '\n')
print('x.shape: ', x.shape, '\n' )
print('b: \n', b , '\n')
print('b.shape: ', b.shape, '\n' )
print('A: \n', A, '\n')
print('A.shape: ', A.shape, '\n' )
print('K(A)=', condA, '\n')

# decomposizione di Choleski
L = scipy.linalg.cholesky(A, lower = True)
print('L:', L, '\n')

print('L.T*L =', scipy.linalg.norm(A-np.matmul(np.transpose(L),L)))
print('err = ', scipy.linalg.norm(A-np.matmul(np.transpose(L),L), 'fro'))

y = scipy.linalg.solve_triangular(L, b, lower = True)
my_x = scipy.linalg.solve_triangular(L.T, y, lower = False)

print('my_x = \n ', my_x)

print('norm =', np.linalg.norm(x-my_x, 'fro'))


K_A = np.zeros((6,1))
Err = np.zeros((6,1))

for n in np.arange(5,11):
    # crazione dati e problema test
    A = scipy.linalg.hilbert(n)
    x = np.ones(n)
    b = np.dot(A,x)
    
    # numero di condizione 
    K_A[n-5] = np.linalg.cond(A)
    
    # fattorizzazione 
    L = scipy.linalg.cholesky(A, lower = True)
    y = scipy.linalg.solve_triangular(L, b, lower = True)
    my_x = scipy.linalg.solve_triangular(L.T, y, lower = False )
    
    # errore relativo
    Err[n-5] = np.linalg.norm(x-my_x, 2)/np.linalg.norm(x, 2)
  
xplot = np.arange(5,11)

# grafico del numero di condizione vs dim
plt.semilogy(xplot, K_A)
plt.title('CONDIZIONAMENTO DI A ')
plt.xlabel('dimensione matrice: n')
plt.ylabel('K(A)')
plt.show()


# grafico errore in norma 2 in funzione della dimensione del sistema
plt.plot(xplot, Err)
plt.title('Errore relativo')
plt.xlabel('dimensione matrice: n')
plt.ylabel('Err= ||my_x-x||/||x||')
plt.show()
