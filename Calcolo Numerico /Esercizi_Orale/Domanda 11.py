" 11. Metodo del gradiente "

import numpy as np
import matplotlib.pyplot as plt

def next_step(x,grad): # backtracking procedure for the choice of the steplength, prende in input il punto nel quale si cerca di minimizzare la funzione e il gradiente della funzione nel punto x
  alpha=1.1 # passo iniziale
  rho = 0.5 # fattore di riduzione per aggiornare alpha in caso la condizione di Armijo non sia soddisfatta
  c1 = 0.25 # parametro della condizione di Armijo (0<c1<1)
  p=-grad # direzione di discesa, antigradiente
  j=0 # contatore che tiene traccia del numero di iterazioni
  jmax=10
  
  while ((f(x+alpha*p) > f(x)+c1*alpha*np.dot(grad,p)) and j<jmax ): #condizione di Armijo
    alpha= rho*alpha
    j+=1
  if (j>jmax):
    return -1 # la procedura non è riuscita a trovare un passo soddisfacente entro il numero massimo di iterazioni
  else:
    print('alpha=',alpha)
    return alpha 

# Se la procedura di backtracking termina prima di raggiungere il numero massimo di iterazioni, allora è stata trovata una lunghezza del passo che soddisfa Armijo. Dunque la funzione next_step restituisce il valore calcolato di alpha
# Il valore di alpha restituito è sufficientemente piccolo da garantire una discesa lungo la direzione dell'anti gradiente


def minimize(f,grad_f,x0,step,maxit,tol,xTrue,fixed=True): # minimizzazione di f con il metodo del gradiente (passo fisso o backtracking, a seconda del valore del parametro fixed); prende in input la stima iniziale della soluzione, la dimensione del passo, la tolleranza (condizione di arresto dell'algoritmo, che continuerà ad iterare fintanto che la norma del gradiente è maggiore di questa tolleranza),la soluzione vera 
  x_list=np.zeros((2,maxit+1)) # matrice contenente le stime della soluzione a ogni iterazione. La prima colonna è inizializzata con la stima iniziale x0

  norm_grad_list=np.zeros(maxit+1) # array che tiene traccia delle norme del gradiente a ogni iterazione
  function_eval_list=np.zeros(maxit+1) # array che tiene traccia dei valori della funzione a ogni iterazione
  error_list=np.zeros(maxit+1) # array che tiene traccia delle norme degli errori tra le stime e la soluzione vera a ogni iterazione. L'elemento iniziale ([0]) è la norma dell'errore tra x0 e la soluzione vera xTrue
  
  #initialize first values
  x_last = x0 # inizializza la variabile con la stima iniziale x0 (soluzione corrente durante le iterazioni)

  x_list[:,0] = x_last # assegna i valori della stima corrente x_last alla prima colonna della matrice x_list; x_list tiene traccia delle stime della soluzione a ogni iterazione
  
  k=0 # contatore che tiene traccia del numero di iterazioni

  function_eval_list[k]=f(x0) # calcola il valore di f nella stima iniziale x0 e lo assegna all'elemento corrispondente nella lista. In questo modo conterrà i valori della funzione a ogni iterazione
  error_list[k]=np.linalg.norm(x_last-xTrue) # calcola la norma dell'errore tra la stima corrente e la soluzione vera xTrue e lo assegna all'elemento corrispondente nella lista. Questa lista conterrà le norme degli errori a ogni iterazion
  norm_grad_list[k]=np.linalg.norm(grad_f(x0)) # calcola la norma del gradiente nella stima iniziale x0 e lo assegna all'elemento corrispondente nella lista. In questo modo conterrà le norme del gradiente a ogni iterazione

  while (np.linalg.norm(grad_f(x_last))>tol and k < maxit ): #  Il ciclo continua fintanto che entrambe le condizioni sono verificate; termina quando una delle condizioni (convergenza o raggiungimento numero massimo di iterazioni) è soddisfatta 
    k=k+1
    grad = grad_f(x_last) # calcola il gradiente di f nella posizione corrente x_last
    
    
    if not fixed:
        step = next_step(x_last, grad) 
        # verifica se l'argomento fixed è False. se è False, viene chiamata la funzione next_step, l'algoritmo sta utilizzando backtracking
        # se fixed è True, la lunghezza del passo è fissata 
        
    if(step==-1):
      print('Non convergente')
      return (k) 
  # se il backtracking non converge entro un certo numero di iterazioni, si stampa "Non convergente" e la funzione restituisce il numero totale di iterazioni k

    x_last=x_last-step*grad # Aggiorna la stima corrente x_last usando il passo calcolato
    
    x_list[:,k] = x_last # Aggiorna la matrice x_list con la nuova stima

    function_eval_list[k]=f(x_last) # calcola il valore di f nella nuova stima e lo assegna all'elemento corrispondente nella lista 
    error_list[k]=np.linalg.norm(x_last-xTrue) # calcola la norma dell'errore tra la nuova stima e la soluzione vera xTrue e lo assegna all'elemento corrispondente nella lista
    norm_grad_list[k]=np.linalg.norm(grad_f(x_last)) # calcola la norma del gradiente nella nuova stima e lo assegna all'elemento corrispondente nella lista

  function_eval_list = function_eval_list[:k+1]
  error_list = error_list[:k+1]
  norm_grad_list = norm_grad_list[:k+1]
  # liste ridimensionate per contenere gli elementi fino alla k-esima iterazione, (il ciclo può terminare prima di maxit iterazioni)
  
  print('Iterazioni totali = ', k)
  print('Last guess: x = (%f,%f)'%(x_list[0,k],x_list[1,k])) # stampa l'ultima approssimazione ottenuta. La stringa (%f,%f) viene utilizzata per formattare la stampa in modo che visualizzi i valori delle due coordinate della soluzione. %f indica la formattazione di un numero in virgola mobile
 
  return (x_last, norm_grad_list, function_eval_list, error_list, x_list, k)
# ultima stima della soluzione, lista contenente le norme del gradiente a ogni iterazione
# lista contenente i valori della funzione a ogni iterazione, lista contenente le norme degli errori tra le stime e la soluzione vera a ogni iterazione
# matrice che registra le stime della soluzione a ogni iterazione, e il numero di iterazioni effettuate


def f(vec):
    x, y = vec
    fout = 3*(x-2)**2+(y-1)**2
    return fout

def grad_f(vec):
    x, y = vec
    dfdx = 6*(x-2)
    dfdy = 2*(y-1)
    return np.array([dfdx,dfdy])

x = np.linspace(-1.5, 5.5)
y = np.linspace(-1, 5, 100)

X, Y = np.meshgrid(x, y) # crea una griglia bidimensionale di coordinate a partire dai vettori unidimensionali x e y 
vec = np.array([X,Y]) # array bidimensionale in cui ogni colonna rappresenta le coordinate (x, y) di un punto sulla griglia
Z=f(vec) #  applica f a ciascun punto della griglia rappresentato da vec. Z sarà un array bidimensionale che contiene i valori della funzione f calcolati su ogni punto della griglia

fig = plt.figure(figsize=(15, 8))

ax = plt.axes(projection='3d') # disegna il grafico tridimensionale
ax.set_title('$f(x)=(x-1)^2 + (y-2)^2$')
s = ax.plot_surface(X, Y, Z, cmap='viridis') # utilizza il metodo plot_surface per generare la superficie tridimensionale del grafico
fig.colorbar(s) # aggiunge una barra dei colori alla destra del grafico per visualizzare la corrispondenza tra i colori e i valori della funzione sulla superficie
plt.show()

fig = plt.figure(figsize=(8, 5))
contours = plt.contour(X, Y, Z, levels=1000)
plt.title('Contour plot $f(x)=(x-1)^2 + (y-2)^2$')
fig.colorbar(contours)


step = 0.002 # dimensione del passo
maxitS= 1000 
tol=1.e-5 # tolleranza, l'algoritmo che continuerà ad iterare fintanto che la norma del gradiente sarà maggiore di questa tolleranza
x0 = np.array([3, 5]) # punto di partenza dell'algoritmo di ottimizzazione
xTrue = np.array([2, 1]) # valore vero 

print("\nMetodo gradiente passo fisso: ")

(x_last,norm_grad_listf, function_eval_listf, error_listf, xlist, k)= minimize(f,grad_f,x0,step,maxitS,tol,xTrue,fixed=True) 
print("Norma errore:", np.linalg.norm(x_last-xTrue, 2))
plt.plot(xlist[0, :k], xlist[1, :k],'*-') # Plotta il percorso dell'ottimizzazione nel piano 2D. xlist contiene le coordinate (x, y) della soluzione in ogni iterazione, e :k assicura che vengano plottate solo le iterazioni effettivamente eseguite (fino a k)


print("\nMetodo gradiente backtracking: ")

(x_last,norm_grad_list, function_eval_list, error_list, xlist, k)= minimize(f,grad_f,x0,step,maxitS,tol,xTrue,fixed=False) #backtracking
print("Norma errore:", np.linalg.norm(x_last-xTrue, 2))
plt.plot(xlist[0, :k], xlist[1, :k],'*-') # genera un grafico che mostra i primi k punti della lista xlist nel piano
plt.legend(['fixed', 'backtracking'])

plt.show()

fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
ax1.semilogy(norm_grad_listf) # scala logaritmica
ax1.semilogy(norm_grad_list)
ax1.set_title('$\|\\nabla f(x_k)\|$')
ax2.semilogy(function_eval_listf)
ax2.semilogy(function_eval_list)
ax2.set_title('$f(x_k)$')
ax3.semilogy(error_listf)
ax3.semilogy(error_list)
ax3.set_title('$\|x_k-x^*\|$')
fig.tight_layout()
fig.legend(['fixed', 'backtracking'], loc='lower center', ncol=4)
plt.show()



# Metodo del gradiente con passo fisso e con backtracking per minimizzare una 
# funzione di due variabili. 

# 1. Funzione Obiettivo e Gradiente:
# La funzione obiettivo e il suo gradiente sono definiti.
# La funzione obiettivo è visualizzata tramite un grafico 3D e un grafico di contorno.

# 2. Metodo del Gradiente con Passo Fisso e Backtracking:
# - minimize implementa il metodo del gradiente con la possibilità di scegliere
#   tra un passo fisso e l'utilizzo del backtracking.

# - next_step implementa la procedura di backtracking per la scelta della
#   lunghezza del passo.

# - Viene fornito un criterio di arresto basato sulla norma del gradiente o sul
#   numero massimo di iterazioni.

# - Vengono memorizzati e visualizzati i risultati come la norma del gradiente, il
# valore della funzione, l'errore rispetto alla soluzione vera e la traiettoria della
# ricerca durante le iterazioni.

# 3. Esecuzione del Metodo del Gradiente:
# - Il metodo del gradiente è eseguito sia con un passo fisso che con il backtracking.
# - La traiettoria della ricerca è visualizzata su un grafico di contorno.

# 4. Analisi dei Risultati:
# I risultati del metodo del gradiente con passo fisso e backtracking sono
# confrontati attraverso grafici delle norme del gradiente, del valore della
# funzione e dell'errore rispetto alla soluzione vera.

