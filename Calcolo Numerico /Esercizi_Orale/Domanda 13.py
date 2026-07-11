" 13. Deblur "

import numpy as np
import matplotlib.pyplot as plt
from skimage import data, metrics
from utils_SR import psf_fft, A, AT, gaussian_kernel, totvar 

X = data.camera().astype(np.float64) / 255 # immagine in floating point con valori tra 0 e 1
m, n = X.shape # variabili per memorizzare le dimensioni dell'immagine

# Genera il filtro di blur
plt.title("Kernel gaussiano")
k = gaussian_kernel(24, 3) # crea un kernel gaussiano basato sulle dimensioni e sulla varianza 
plt.imshow(k)
plt.show()

# Blur with FFT; calcola la trasformata di Fourier del kernel gaussiano
plt.title("FFT del kernel gaussiano")
K = psf_fft(k, 24, X.shape) 
plt.imshow(np.abs(K)) # calcola il modulo di questa rappresentazione nelle frequenze
plt.show()

# esegue una convoluzione tra l'immagine originale X e il kernel K
X_blurred = A(X, K, 1)  # A: funzione di convoluzione. X_blurred contiene l'immagine originale dopo essere stata sfocata con il kernel gaussiano
plt.subplot(121).imshow(X, cmap='gray', vmin=0, vmax=1)
plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122).imshow(X_blurred, cmap='gray', vmin=0, vmax=1)
plt.title('Blurred')
plt.xticks([]), plt.yticks([])
plt.show()

# Genera il rumore e lo aggiunge all'immagine sfocata
sigma = 0.02 # definisce la deviazione standard della distribuzione normale che verrà utilizzata per generare il rumore. Maggiore è sigma, maggiore sarà l'ampiezza del rumore
np.random.seed(42) # rende riproducibili i risultati
noise = np.random.normal(size=X_blurred.shape) * sigma # genera un array di rumore con le stesse dimensioni di X_blurred. np.random.normal restituisce campioni da una distribuzione normale con media zero e deviazione standard uno. L'array noise è aggiunto all'immagine sfocata

# Aggiungi blur e rumore per ottenere l'immagine corrotta y
y = X_blurred + noise
ATy = AT(y, K, 1) # operazione di deconvoluzione, per ottenere una stima dell'immagine originale X (stima che può essere confrontata con l'immagine originale per valutare la qualità della ricostruzione, calcolando PSNR o MSE)

PSNR = metrics.peak_signal_noise_ratio(X, ATy)
mse = metrics.mean_squared_error(X, ATy)

# Visualizziamo i risultati
plt.figure(figsize=(30, 10))
plt.subplot(121).imshow(X, cmap='gray', vmin=0, vmax=1)
plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122).imshow(y, cmap='gray', vmin=0, vmax=1)
plt.title(f'Corrupted: (PSNR: {PSNR:.3f}), (MSE: {mse:.3f})')
plt.xticks([]), plt.yticks([])
plt.show()


# Soluzione naive
from scipy.optimize import minimize

# Funzione che si sta minimizzando
def f(x):
    x = x.reshape((m, n)) # vettore dei pixel dell'immagine, ridimensionato in una matrice; deve essere trattato come un'immagine nella successiva operazione di convoluzione
    Ax = A(x, K, 1) # immagine deconvoluta, ottenuta applicando l'operatore di convoluzione inversa A al vettore dei pixel x utilizzando il kernel K
    return 0.5 * np.sum(np.square(Ax - y)) # Ax - y: differenza pixel per pixel tra l'immagine deconvoluta e l'immagine corrotta 
                                           # np.square calcola il quadrato di ciascuna differenza
                                           # np.sum calcola la somma di tutti i quadrati delle differenze, moltiplicata poi per 0.5
# Il risultato è una misura della discrepanza tra l'immagine deconvoluta e l'immagine corrotta

# Gradiente della funzione, rispetto al valore del pixel x, da minimizzare
def df(x):
    x = x.reshape((m, n))
    ATAx = AT(A(x, K, 1), K, 1) # AT(A(x, K, 1), K, 1): applicazione dell'operatore di convoluzione inversa AT a A(x, K, 1)
                                # A(x, K, 1): applicazione dell'operatore di convoluzione A al vettore dei pixel x usando il kernel K
    d = ATAx - ATy # differenza pixel per pixel tra l'immagine deconvoluta e l'immagine corrotta
    return d.reshape(m * n) # il risultato d viene appiattito in un vettore con e restituito come il gradiente della funzione rispetto ai pixel x
# Questo gradiente verrà utilizzato nel metodo di discesa del gradiente coniugato, per guidare la ricerca della soluzione ottimale durante il processo di minimizzazione della funzione

# Minimizzazione della funzione
x0 = ATy.reshape(m * n) # inizializza il vettore dei pixel con la forma piatta di ATy (immagine corrotta deconvoluta)
max_iter = 25
res = minimize(f, x0, method='CG', jac=df, options={'maxiter': max_iter, 'return_all': True}) # esegue l'ottimizzazione utilizzando il metodo del gradiente coniugato, il parametro jac=df specifica che viene fornito il gradiente della funzione, 'return_all': restituisce tutte le iterazioni 
# l'obiettivo è ridurre il divario tra l'immagine deconvoluta (Ax) e l'immagine corrotta (y); si cercano i pixel dell'immagine che minimizzano questa discrepanza

# Per ogni iterazione calcola PSNR e mse rispetto all'originale
PSNR = np.zeros(max_iter + 1) #  Inizializza un vettore di zeri per contenere i valori del PSNR ad ogni iterazione
mse = np.zeros(max_iter + 1)

for k, x_k in enumerate(res.allvecs): # itera su tutte le soluzioni trovate durante le iterazioni ottimizzate
    PSNR[k] = metrics.peak_signal_noise_ratio(X, x_k.reshape(X.shape)) # Calcola il PSNR tra l'immagine originale X e l'immagine ricostruita x_k all'iterazione k, quindi salva il risultato nel vettore PSNR all'indice k
    mse[k] = metrics.mean_squared_error(X, x_k.reshape(X.shape))

# Risultato della minimizzazione
X_res = res.x.reshape((m, n)) # prende il vettore risultante dalla minimizzazione res.x e lo ridimensiona in una matrice delle dimensioni originali dell'immagine (m, n). Questo è fatto perché il risultato dell'ottimizzazione è rappresentato come un vettore, ma per visualizzare l'immagine ricostruita è utile avere la forma bidimensionale corretta
# X_res contiene l'immagine ricostruita ottenuta dalla minimizzazione, e viene utilizzata successivamente per visualizzare l'immagine ricostruita e calcolare misure di qualità come PSNR e MSE

# PSNR e mse dell'immagine corrotta rispetto all'originale
starting_PSNR = np.full(PSNR.shape[0], metrics.peak_signal_noise_ratio(X, ATy)) # calcola PSNR tra l'immagine originale X e l'immagine deconvoluta ATy e crea un array in cui ogni elemento è impostato sullo stesso valore del PSNR tra l'immagine originale e l'immagine deconvoluta corrotta (avere un punto di riferimento per il confronto, poiché starting_PSNR rappresenta il PSNR dell'immagine corrotta prima della deconvoluzione)
starting_mse = np.full(mse.shape[0], metrics.mean_squared_error(X, ATy)) # mse.shape[0]: restituisce la lunghezza dell'array, che rappresenta l'evoluzione dell'MSE durante le iterazioni di ottimizzazione; valore utilizzato per determinare la lunghezza dell'array 
                                                                         # np.full(mse.shape[0], ...): crea un array di dimensione mse.shape[0] e lo inizializza con il valore specificato come secondo argomento
                                                                         # metrics.mean_squared_error(X, ATy): calcola mse tra l'immagine originale X e l'immagine deconvoluta ATy. Questo valore viene utilizzato per inizializzare tutti gli elementi dell'array
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

ax1.plot(PSNR, '-*', label="Soluzione naive")
ax1.plot(starting_PSNR, label="Immagine corrotta")
ax1.legend()
ax1.set_title('PSNR per iterazione (LSQ)')
ax1.set_ylabel("PSNR")
ax1.set_xlabel('itr')

ax2.plot(mse, '-*', label="Soluzione naive")
ax2.plot(starting_mse, label="Immagine corrotta")
ax2.legend()
ax2.set_title('MSE per iterazione (LSQ)')
ax2.set_ylabel("MSE")
ax2.set_xlabel('itr')

ax3.imshow(X_res, cmap='gray', vmin=0, vmax=1)
ax3.set_title('Immagine Ricostruita (LSQ)')
ax3.set_xticks([]), ax2.set_yticks([])

plt.show()

# Regolarizzazione
# Funzione da minimizzare
def f(x, L):
    x = x.reshape((m, n)) # x variabile di ottimizzazione, è una matrice che viene plasmata per rappresentare l'immagine
    nsq = totvar(x) # calcola la norma quadratica totale dell'immagine x
    Ax = A(x, K, 1) # calcola l'immagine deconvoluta Ax 
    return 0.5 * np.sum(np.square(Ax - y)) + 0.5 * L * nsq # 0.5 * np.sum(np.square(Ax - y)): misura la discrepanza tra l'immagine deconvoluta Ax e l'immagine osservata y
                                                           # + 0.5 * L * nsq: termine di regolarizzazione di Tikhonov. nsq e la norma quadratica totale dell'immagine ricostruita (λ/2 * ∥x∥^2)
# la funzione f(x, L) cerca di minimizzare la discrepanza tra l'immagine deconvoluta e l'immagine osservata

# Gradiente della funzione da minimizzare
def df(x, L):
    Lx = L * x # prodotto tra L e la variabile di ottimizzazione x
    x = x.reshape(m, n)
    ATAx = AT(A(x, K, 1), K, 1) # Calcola il prodotto ATAx dell'operatore di trasposizione AT applicato all'operatore di avvicinamento A alla variabile di ottimizzazione x con il kernel K. Questo termine rappresenta la derivata parziale della funzione rispetto a x
    d = ATAx - ATy 
    return d.reshape(m * n) + Lx # restituisce il vettore della derivata parziale sommando l'errore d plasmato come vettore e il contributo della penalizzazione Lx


x0 = ATy.reshape(m * n) # ATy è l'immagine deconvoluta convertita in vettore, utilizzato come punto di partenza per l'ottimizzazione
lambdas = [0.0001, 0.0005, 0.001, 0.05, 0.5, 1] # valori di regolarizzazione
PSNRs = [] # liste vuote per memorizzare 
mses = []
images = []

# Ricostruzione per diversi valori del parametro di regolarizzazione
for i, L in enumerate(lambdas): # itera attraverso gli elementi della lista lambdas, ottenendo sia il valore di lambda che l'indice corrispondente
    max_iter = 50 
    res = minimize(f, x0, (L), method='CG', jac=df, options={'maxiter': max_iter}) #  minimizza la funzione f con il metodo del gradiente coniugato. Vengono forniti il punto di partenza, il valore di lambda L, la funzione del gradiente. I risultati sono memorizzati nella variabile res

    # Aggiungi la ricostruzione nella lista images
    X_curr = res.x.reshape(X.shape) # la soluzione ottimale res.x viene convertita in un array per ottenere l'immagine ricostruita X_curr, che viene poi aggiunta alla lista images
    images.append(X_curr)

    # Stampa il PSNR e l'mse per il valore di lambda attuale
    PSNR = metrics.peak_signal_noise_ratio(X, X_curr)
    mse = metrics.mean_squared_error(X, X_curr)

    PSNRs.append(PSNR)
    mses.append(mse)
    print(f'PSNR: {PSNR:.3f} (\u03BB = {L})')
    print(f'MSE: {mse:.3f} (\u03BB = {L})')
    print('\n')
    #vengono calcolati il PSNR e l'MSE tra l'immagine originale X e l'immagine ricostruita X_curr. Questi valori vengono aggiunti alle liste PSNRs e mses, e vengono stampati a schermo insieme al valore corrente di lambda

# Visualizziamo i risultati
plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.plot(lambdas, PSNRs, '-*')
plt.title('PSNR per $\lambda$')
plt.ylabel("PSNR")
plt.xlabel('$\lambda$')

plt.subplot(122)
plt.plot(lambdas, mses, '-m*')
plt.title('MSE per $\lambda$')
plt.ylabel("MSE")
plt.xlabel('$\lambda$')
plt.show()

plt.figure(figsize=(30, 10))

plt.subplot(1, len(lambdas) + 2, 1).imshow(X, cmap='gray', vmin=0, vmax=1)
plt.title("Originale")
plt.xticks([]), plt.yticks([])
plt.subplot(1, len(lambdas) + 2, 2).imshow(y, cmap='gray', vmin=0, vmax=1)
plt.title("Corrotta")
plt.xticks([]), plt.yticks([])

for i, L in enumerate(lambdas):
    plt.subplot(1, len(lambdas) + 2, i + 3).imshow(images[i], cmap='gray', vmin=0, vmax=1)
    plt.title(f"Ricostruzione ($\lambda$ = {L:.4f})")
plt.show()
# crea una figura contenente subplot per ciascun valore di lambda, mostrando le relative immagini ricostruite con i titoli corrispondenti



# Il codice implementa la ricostruzione di un'immagine corrotta utilizzando la minimizzazione di una funzione obiettivo. Ecco una panoramica del codice:

# Generazione dell'immagine di input:
# Viene utilizzata un'immagine di esempio dal modulo data di skimage.
# Viene creato un kernel gaussiano di dimensioni 24x24 con varianza 3 e ne viene mostrato l'andamento.
# Generazione del kernel di blur:
# Viene mostrata la rappresentazione FFT del kernel gaussiano.
# Blurring dell'immagine di input:
# L'immagine originale viene sfocata utilizzando il kernel gaussiano con l'operazione di convoluzione.
# Viene mostrata l'immagine originale e quella sfocata.
# Aggiunta di rumore:
# Viene generato del rumore gaussiano e aggiunto all'immagine sfocata per simulare una situazione realistica.
# Viene calcolato il PSNR tra l'immagine originale e quella corrotta.
# Soluzione naive senza regolarizzazione:
# Viene definita la funzione da minimizzare, che rappresenta la somma dei quadrati degli errori tra l'immagine ricostruita e quella corrotta.
# Viene utilizzato l'ottimizzatore minimize di SciPy per minimizzare la funzione.
# Vengono tracciati il PSNR e l'MSE per ogni iterazione della minimizzazione.
# Viene mostrata l'immagine ricostruita.
# Regolarizzazione con variazione totale (Total Variation):
# Viene definita una funzione obiettivo che include un termine di regolarizzazione basato sulla variazione totale dell'immagine.
# La minimizzazione viene eseguita per diversi valori di lambda, che controllano l'importanza del termine di regolarizzazione.
# Vengono tracciati il PSNR e l'MSE per ogni valore di lambda.
# Vengono mostrate le immagini ricostruite per diversi valori di lambda.
# In generale, il codice mostra l'effetto della regolarizzazione sulla ricostruzione di un'immagine corrotta, consentendo di trovare un buon compromesso tra fedeltà alla data corrotta e regolarizzazione dell'immagine risultante.
