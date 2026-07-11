import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
from scipy.linalg import lu_factor as LUdec 

# Exercise 1

m = 100
n = 10

A = np.random.rand(m, n)

alpha_test = np.ones(n) #vettore di dimensione n
y = A @ alpha_test

print('alpha test', alpha_test)

ATA = A.T@A
ATy = A.T@y

lu, piv = LUdec(ATA)
alpha_LU = scipy.linalg.lu_solve((lu,piv), ATy)

print('alpha LU', alpha_LU)

L = scipy.linalg.cholesky(ATA) #A trasposto A
x = scipy.linalg.solve_triangular(np.transpose(L), ATy, lower=True)
alpha_chol = scipy.linalg.solve_triangular(L, x, lower=False)

print('alpha chol', alpha_chol)

U, s, Vh = scipy.linalg.svd(A)

print('Shape of U:', U.shape)
print('Shape of s:', s.shape)
print('Shape of V:', Vh.T.shape)

alpha_svd = np.zeros(s.shape)

for i in range(n):
  ui = U[:, i]
  vi = Vh[i, :]

  alpha_svd = alpha_svd + (np.dot(ui, y) * vi) / s[i]
  #OPPURE ((ui.T @ y) * vi) / s[i]

print('alpha SVD', alpha_svd)


# Exercise 2
case = 0 #da far variare in caso 0, 1, 2
m = 10
m_plot = 100

# Grado polinomio approssimante
n = 5 #far variare il grado tra 1, 2, 3, 5, 7

if case==0:
    x = np.linspace(-1,1,m) #vettore/intervallo di m punti equispaziati tra -1, 1
    y = np.exp(x/2)
elif case==1:
    x = np.linspace(-1,1,m)
    y = 1/(1+25*(x**2))
elif case==2:
    x = np.linspace(0,2*np.pi,m) 
    y = np.sin(x)+np.cos(x)


A = np.zeros((m, n+1)) #m righe, n+1 elementi relativi ai coefficienti del termine noto e termine noto

for i in range(n+1): #costruisce la marice A di dimensione (m*n+1)
  A[:, i] = x**i
  
U, s, Vh = scipy.linalg.svd(A) #dato che non è una matrice quadrata, uso la svd per la decomposizione


alpha_svd = np.zeros(n+1)

for i in range(n+1): #formula della decomposizione (sommatoria)
  ui = U[:, i]
  vi = Vh[i, :]

  alpha_svd = alpha_svd + np.dot(ui, y) * vi /s[i] #soluzione del problema ai minimo quadrati usando la svd

print(alpha_svd)

#x: dati da approssimare 
#x_plot: vettore con estremi minimo e massimo di x per fare il grafico 
x_plot = np.linspace(x[0], x[-1], m_plot) #punti in cui si valuta sia la funzione che il polinomio
A_plot = np.zeros((m_plot, n+1)) #matrice in cui si valuta il polinomio, dove i coefficienti sono noti

for i in range(n+1):
  A_plot[:, i] = x_plot**i

y_interpolation = A_plot @ alpha_svd

plt.plot(x, y, 'o')
plt.plot(x_plot, y_interpolation, 'r')
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Approssimazione polinomiale di grado {n}')
plt.grid()
plt.show()


res = np.linalg.norm(A @ alpha_svd - y)
print('Residual: ', res)

#man mano che il polinomio ha grado maggiore, la funzione viene approssimata meglio