" 5., 6., 7. Approssimazione dati ai minimi quadrati "

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
#from scipy.linalg import lu_factor as LUdec 
  
case = 0 
m = 10 # numero di nodi di interpolazione
m_plot = 100 # numero di punti utilizzati per valutare le funzioni


if case==0:
    x = np.linspace(-1,1,m) # vettore di nodi di interpolazione equispaziati tra -1, 1
    y = np.exp(x/2) # valori della funzione da approssimare
    f = lambda x: np.exp(x*(1/2)) # la funzione lambda definisce funzioni senza un nome definito; f diventa una funzione che prende un argomento x e restituisce l'esponenziale
elif case==1:
    x = np.linspace(-1,1,m)
    y = 1/(1+25*(x**2))
    f = lambda x: 1/(1+25*(x**2))
elif case==2:
    x = np.linspace(0,2*np.pi,m) 
    y = np.sin(x)+np.cos(x)
    f = lambda x: np.sin(x)+ np.cos(x)
    
    
for n in [1, 2, 3, 5, 7]: # lista di gradi del polinomio
    A = np.zeros((m, n+1)) # Viene inizializzata la matrice di Vandermonde con dimensioni (m, n+1), con m numero di nodi di interpolazione e n+1 numero di coefficienti del polinomio 
   
    #METODO SVD
    for i in range(n+1): 
        A[:, i] = x**i # crea la matrice di Vandermonde; Per ogni grado i del polinomio:
                       # x**i calcola un vettore che contiene gli elementi di x elevati alla potenza i.
                       # A[:, i] assegna questo vettore come colonna i della matrice A
   
    U, s, Vh = scipy.linalg.svd(A) 
    alpha_svd = np.zeros(n+1) # inizializza un vettore di zeri, utilizzato per memorizzare i coefficienti del polinomio ottenuti dalla SVD
                              # la dimensione del vettore è (n+1) perché si sta approssimando un polinomio di grado massimo n
   
    for i in range(n+1): 
        ui = U[:, i]
        vi = Vh[i, :]
        alpha_svd = alpha_svd + np.dot(ui, y) * vi /s[i] # calcola e aggiorna i coefficienti del polinomio utilizzando la SVD per risolvere il problema ai minimi quadrati


    x_plot = np.linspace(x[0], x[-1], m_plot) # Crea un vettore x_plot di m_plot punti equispaziati tra il primo (x[0]) e l'ultimo (x[-1]) valore del vettore x. Rappresenta i punti in cui si valutano funzione e polinomio
    A_plot = np.zeros((m_plot, n+1)) # Inizializza una matrice A_plot di dimensioni (m_plot, n+1) con tutti gli elementi a zero; verrà utilizzata per valutare il polinomio approssimato in più punti

    for i in range(n+1): #costruisce A_plot[:, i] per valutare la funzione in molti più punti
        A_plot[:, i] = x_plot**i

    y_interpolationSVD = A_plot @ alpha_svd # punti di valutazione del polinomio approssimato utilizzando la SVD nei punti specificati in x_plot
    
    # METODO EQUAZIONI NORMALI 
    ATA = A.T@A
    ATy = A.T@y
    
    L = scipy.linalg.cholesky(ATA) # decomposizione di cholesky della matrice ATA (L)
    z = scipy.linalg.solve_triangular(np.transpose(L), ATy, lower=True) #risolve il sistema lineare inferiore triangolare, Lz = ATy
    alpha_chol = scipy.linalg.solve_triangular(L, z, lower=False) #risolve il sistema lineare superiore triangolare, L^T alpha_chol = z; coefficienti del polinomio
    
    y_interpolationChol = A_plot @ alpha_chol # calcola i valori interpolati del polinomio approssimato nei punti specificati da A_plot utilizzando i coefficienti calcolati
    
    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1)
    plt.title(f"Equazioni normali grado={i}") # f-string consente di inserire il valore della variabile i all'interno della stringa
    plt.plot(x, y, 'o')
    plt.plot(x_plot, f(x_plot), 'blue')
    plt.plot(x_plot, y_interpolationChol, label=f"Risoluzione con EQ normali, grado={i}", color='green')
    plt.grid()
    
    plt.subplot(1, 2, 2)
    plt.title(f"SVD grado={i}")
    plt.plot(x, y, 'o')
    plt.plot(x_plot, f(x_plot), 'blue')
    plt.plot(x_plot, y_interpolationSVD, label=f"Risoluzione con SVD, grado={i}", color='green')
    plt.grid()
    plt.show()
    
    
    err1 = np.linalg.norm(A @ alpha_svd - y, 2) # Calcola la norma 2 dell'errore tra i dati originali y e i dati approssimati calcolati usando la SVD (A @ alpha_svd)
    err2 = np.linalg.norm(A @ alpha_chol - y, 2) # Calcola la norma 2 dell'errore tra i dati originali y e i dati approssimati calcolati usando Cholesky (A @ alpha_chol)
    print (f'Errore di approssimazione con Eq. Normali (Grado {i:n}): ', err1)
    print (f'Errore di approssimazione con SVD (Grado {i:n}): ', err2, '\n')



# Confronto tra due metodi di risoluzione di un problema di interpolazione polinomiale
# per diverse curve di interpolazione.
# Il codice implementa l'interpolazione polinomiale utilizzando le equazioni 
# normali e la decomposizione ai minimi quadrati tramite SVD.

# 1. Scelta funzione da interpolare

# 2. Generazione dei Dati di Interpolazione: Viene generato un insieme di dati di
# interpolazione con m nodi equispaziati sulla curva selezionata.

# 3. Interpolazione con Equazioni Normali e SVD: Per ogni grado n specificato nel
# loop, il codice costruisce una matrice A delle equazioni del sistema e risolve il
# problema di interpolazione utilizzando:
# - Equazioni Normali
# - SVD

# 4. Visualizzazione dei Risultati: Vengono visualizzati i dati originali, la curva
# esatta e le curve di interpolazione ottenute con entrambi i metodi.

# 5. Calcolo degli Errori: Viene calcolato l'errore di approssimazione per ciascun
# metodo.

# 6. Risultati e Confronto: I risultati delle interpolazioni vengono visualizzati a
# confronto, e gli errori di approssimazione sono stampati a video per confrontare
# le performance dei due metodi.

