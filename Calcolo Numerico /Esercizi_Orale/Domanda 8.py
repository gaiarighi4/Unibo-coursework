" 8. Calcolo zero di funzione "

import numpy as np
import matplotlib.pyplot as plt

def succ_app(f, g, tolf, tolx, maxit, xTrue, x0=0): #f: funzione di cui si cerca lo zero, g: funzione delle approssimazioni successive, tolf: tolleranza sulla funzione, tolx: tolleranza sulla variabile indipendente (quando considerare il risultato accettabile), xTrue: vero zero della funzione  
  i=0 # contatore che tiene traccia del numero di iterazioni nella ricerca dello zero di funzione  
  err=np.zeros(maxit+1, dtype=np.float64) # array utilizzato per memorizzare le differenze tra iterati successivi, ossia |xk - xk-1| 
  err[0]=tolx+1 # inizializza il primo elemento dell'array a un valore maggiore di tolx (per garantire che la condizione err[i] > tolx sia verificata alla prima iterazione del ciclo; assicura che il ciclo inizi eseguendo almeno una volta)
  vecErrore=np.zeros(maxit+1, dtype=np.float64) # array utilizzato per memorizzare l'errore rispetto al vero zero della funzione, ossia |xTrue - xk| 
  vecErrore[0] = np.abs(xTrue - x0) # inizializza il primo elemento dell'array con il valore assoluto della differenza tra xTrue e x0. fornisce un'indicazione iniziale dell'errore rispetto alla soluzione desiderata
  x=x0 # inizializza x al punto iniziale; rappresenta l'iterato corrente nella ricerca dello zero della funzione


  while (i < maxit and ((np.abs(f(x)) > tolf) or err[i] > tolx)): # Il ciclo continua ad eseguire finché:
                                                                  # maxit non è stato raggiunto e
                                                                  # L'errore assoluto della funzione è maggiore di una tolleranza o
                                                                  # L'errore assoluto tra iterati successivi è maggiore di una tolleranza
    
    x_new= g(x) # calcola il nuovo iterato applicando la funzione di iterazione g al valore corrente x
    err[i+1]= np.abs(x_new - x) # calcola e memorizza in posizione i+1 l'errore assoluto tra l'iterato corrente x e il nuovo iterato x_new 
    vecErrore[i+1]=  np.abs(xTrue - x_new) # calcola e memorizza l'errore assoluto tra xTrue e il nuovo iterato x_new nell'array vecErrore
    i=i+1 # incrementa i per tenere traccia del numero di iterazioni
    x=x_new # aggiorna l'iterato corrente x con il nuovo iterato x_new
  err=err[0:i] # ridefinisce l'array per contenere gli elementi fino all'i esima iterazione; assicura che l'array finale contenga solo gli elementi effettivamente calcolati durante il ciclo di iterazioni 
  vecErrore = vecErrore[0:i] 
  return (x, i, err, vecErrore) # vengono restituiti il risultato finale, il numero di iterazioni, gli errori assoluti tra iterati successivi e gli errori assoluti rispetto al vero zero della funzione


def newton(f, df, tolf, tolx, maxit, xTrue, x0=0):
    g = lambda x: x - f(x)/df(x) 
    (x, i, err, vecErrore) = succ_app(f, g, tolf, tolx, maxit, xTrue, x0) # chiama la funzione succ_app passando f, g, le tolleranze, maxit, xTrue e x0. Restituisce l'iterato finale x, il numero totale di iterazioni effettuate i, gli errori assoluti tra iterati successivi err, e gli errori assoluti rispetto allo zero vero della funzione vecErrore
    return (x, i, err, vecErrore) # Restituisce i risultati ottenuti dalla funzione succ_app come risultato della funzione newton


f = lambda x: np.exp(x)-x**2
df = lambda x: np.exp(x) - 2*x 
g1 = lambda x: x-f(x)*np.exp(x/2)
g2 = lambda x: x-f(x)*np.exp(-x/2)

xTrue = -0.703467 # zero della funzione
fTrue = f(xTrue) # valore della funzione calcolata nello zero 
print('\nfTrue = ', fTrue) 
print('\nxTrue = ', xTrue)

xplot = np.linspace(-1, 1) # array di valori equispaziati tra -1 e 1
fplot = f(xplot) # f calcolata nei punti di xplot

plt.plot(xplot,fplot) # traccia la funzione f nei punti specificati in xplot e i corrispondenti valori in fplot. Si crea un grafico della funzione
plt.plot(xTrue,fTrue, 'or', label='True') # punto con coordinate (xTrue, fTrue); rappresenta la posizione dello zero di f 
 
tolx= 10**(-10) # tolleranza sull'errore relativo tra due iterazioni successive. Se la differenza tra due iterazioni successive è inferiore a questa tolleranza, il metodo si ferma
tolf = 10**(-6) # tolleranza sull'errore assoluto della funzione. Se tale valore è inferiore a questa tolleranza, il metodo si ferma
maxit= 100 
x0= 0

[sol_g1, iter_g1, err_g1, vecErrore_g1]=succ_app(f, g1, tolf, tolx, maxit, xTrue, x0)
print(' \n Metodo approssimazioni successive g1 \n x =',sol_g1,'\n iter_g1=', iter_g1) # stampa iterato finale e numero di iterazioni

plt.plot(sol_g1,f(sol_g1), 'o', label='g1')

[sol_g2, iter_g2, err_g2, vecErrore_g2]=succ_app(f, g2, tolf, tolx, maxit, xTrue, x0)
print(' \n Metodo approssimazioni successive g2 \n x =',sol_g2,'\n iter_g2=', iter_g2)

plt.plot(sol_g2,f(sol_g2), 'og', label='g2')

[sol_newton, iter_newton, err_newton, vecErrore_newton]=newton(f, df, tolf, tolx, maxit, xTrue, x0)
print(' \n Metodo Newton \n x =',sol_newton,'\n iter_new=', iter_newton)

plt.plot(sol_newton,f(sol_newton), 'ob', label='Newton')
plt.legend()
plt.grid()
plt.show()

# GRAFICO Errore vs Iterazioni
# g1
plt.plot(vecErrore_g1, '.-', color='blue')

# g2
plt.plot(vecErrore_g2[:20], ".-", color='green') 

# Newton
plt.plot(vecErrore_newton, '.-', color='red')

plt.legend( ("g1", "g2", "newton"))
plt.xlabel('iter')
plt.ylabel('errore')
plt.title('Errore vs Iterazioni')
plt.grid()
plt.show()


# Il codice implementa metodi iterativi per la risoluzione di equazioni non lineari.
# In particolare, sono implementati i metodi di approssimazioni successive e Newton.

# succ_app implementa il metodo di approssimazioni successive.
# newton implementa il metodo di Newton.
# Entrambe le funzioni prendono come argomenti la funzione f(x), la derivata df(x)
# la tolleranza sulla funzione tolf, la tolleranza sulla variabile tolx, il numero
# massimo di iterazioni maxit, il valore vero della soluzione xTrue, e il punto di
# partenza x0 (è 0).

# Il codice utilizza queste funzioni per risolvere tre equazioni non lineari.
# Vengono confrontati i risultati dei due metodi, e il grafico dell'errore rispetto
# alle iterazioni per entrambi i metodi.
