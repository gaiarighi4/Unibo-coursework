" 9. Calcolo zero di funzione "

import numpy as np
import matplotlib.pyplot as plt

def succ_app(f, g, tolf, tolx, maxit, xTrue, x0=0):
  i=0 
  err=np.zeros(maxit+1, dtype=np.float64) #|xk - xk-1|
  err[0]=tolx+1
  vecErrore=np.zeros(maxit+1, dtype=np.float64) 
  vecErrore[0] = np.abs(xTrue - x0)
  x=x0

# cerca di calcolare il punto fisso di g(x), controllando man mano l'errore rispetto
# a xTrue (zero della funzione f) e il valore assoluto di f(x), che devono stare
#dentro a maxit
  while (i < maxit and ((np.abs(f(x)) > tolf) or err[i] > tolx)): # scarto assoluto tra iterati
    x_new= g(x)
    err[i+1]= np.abs(x_new - x)
    vecErrore[i+1]=  np.abs(xTrue - x_new)
    i=i+1
    x=x_new
  err=err[0:i] 
  vecErrore = vecErrore[0:i] 
  return (x, i, err, vecErrore) 

def newton(f, df, tolf, tolx, maxit, xTrue, x0=0):
    g = lambda x: x - f(x)/df(x) 
    (x, i, err, vecErrore) = succ_app(f, g, tolf, tolx, maxit, xTrue, x0)
    return (x, i, err, vecErrore)

f = lambda x: x**3+4*x*np.cos(x)-2
df = lambda x: 3*x**2 + 4*x*-np.sin(x) + 4*np.cos(x) 
g1 = lambda x: (2-x**3)/(4*np.cos(x))

xTrue = 0.536839
fTrue = f(xTrue)
print('fTrue = ', fTrue)

xplot = np.linspace(0, 2)
fplot = f(xplot)

plt.plot(xplot,fplot)
plt.plot(xTrue,fTrue, 'or', label='True')

tolx= 10**(-10)
tolf = 10**(-6)
maxit=100
x0= 1

[sol_g1, iter_g1, err_g1, vecErrore_g1]=succ_app(f, g1, tolf, tolx, maxit, xTrue, x0)
print(' \n Metodo approssimazioni successive g1 \n x =',sol_g1,'\n iter_g1=', iter_g1)

plt.plot(sol_g1,f(sol_g1), '*', label='g1')

[sol_newton, iter_newton, err_newton, vecErrore_newton]=newton(f, df, tolf, tolx, maxit, xTrue, x0)
print(' \n Metodo Newton \n x =',sol_newton,'\n iter_new=', iter_newton)

plt.plot(sol_newton,f(sol_newton), '+b', label='Newton')
plt.grid()
plt.legend()
plt.show()

# GRAFICO Errore vs Iterazioni
# g1
plt.plot(vecErrore_g1, '.-', color='blue')

# Newton
plt.plot(vecErrore_newton, '.-', color='red')

plt.legend( ("g1", "newton"))
plt.xlabel('iter')
plt.ylabel('errore')
plt.title('Errore vs Iterazioni')
plt.grid()
plt.show()


# Domanda 9:
# Calcolo della funzione e della sua derivata.
# Metodo di approssimazioni successive e Newton.
# Vengono confrontati i risultati dei due metodi e viene visualizzato il grafico
# dell'errore rispetto alle iterazioni.

