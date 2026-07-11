" 14. Super Resolution "

import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
from skimage import data, metrics
from scipy import signal
from numpy import fft
#from utils import psf_fft, A, AT, gaussian_kernel
from utils_SR import psf_fft, A, AT, gaussian_kernel, totvar, grad_totvar

# Immagine in floating point con valori tra 0 e 1
X = data.camera().astype(np.float64)/255
m, n = X.shape
sf = 4

# Genera il filtro di blur
plt.title("Kernel gaussiano 24x24 con varianza 3")
k = gaussian_kernel(24, 3)
plt.imshow(k)
plt.show()

# Blur with FFT
plt.title("FFT del kernel gaussiano")
K = psf_fft(k, 24, X.shape)
plt.imshow(np.abs(K))
plt.show()

#Fai AxX sfruttando il fatto che conosco K
X_blurred = A(X, K, sf) 
plt.subplot(121).imshow(X, cmap='gray', vmin=0, vmax=1)
plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122).imshow(X_blurred, cmap='gray', vmin=0, vmax=1) #vmin e vmax indicano i range che vogliamo nel plot
plt.title('Downsampled')
plt.xticks([]), plt.yticks([])
plt.show()


# Genera il rumore
sigma = 0.02
np.random.seed(42)
noise = np.random.normal(size=X_blurred.shape)*sigma

# Aggiungi blur e rumore
y = X_blurred + noise
ATy = AT(y, K, sf)

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

# Funzione da minimizzare
def f(x):
    x = x.reshape((m, n))
    Ax = A(x, K, sf)
    return 0.5 * np.sum(np.square(Ax - y))

# Gradiente della funzione da minimizzare
def df(x):
    x = x.reshape((m, n))
    ATAx = AT(A(x,K, sf),K, sf)
    d = ATAx - ATy 
    return d.reshape(m * n)

# Minimizzazione della funzione
x0 = ATy.reshape(m*n)
max_iter = 25
res = minimize(f, x0, method='CG', jac=df, options={'maxiter':max_iter, 'return_all':True})

# Per ogni iterazione calcola il PSNR rispetto all'originale
PSNR = np.zeros(max_iter + 1)
mse = np.zeros(max_iter + 1)
for k, x_k in enumerate(res.allvecs):
    PSNR[k] = metrics.peak_signal_noise_ratio(X, x_k.reshape(X.shape))
    mse[k]  = metrics.mean_squared_error(X, x_k.reshape(X.shape))


# Risultato della minimizzazione
X_res = res.x.reshape((m, n))

# PSNR e mse dell'immagine corrotta rispetto all'oginale
starting_PSNR = np.full(PSNR.shape[0], metrics.peak_signal_noise_ratio(X, ATy))
starting_mse = np.full(mse.shape[0], metrics.mean_squared_error(X, ATy))


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

ax1.plot(PSNR,'-*', label="Soluzione naive")
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
    x  = x.reshape((m, n))
    nsq = totvar(x) 
    Ax = A(x, K, sf)
    return 0.5 * np.sum(np.square(Ax - y)) + 0.5 * L * nsq

# Gradiente della funzione da minimizzare
def df(x, L):
    Lx = L * x
    x = x.reshape(m, n)
    ATAx = AT(A(x,K, sf),K, sf)
    d = ATAx - ATy
    return d.reshape(m * n) + Lx

x0 = ATy.reshape(m*n)
#lambdas = [0.01,0.03,0.04, 0.06]
lambdas = [0.0001, 0.0005, 0.001, 0.05, 0.5, 1] 
PSNRs = []
mses=[]
images = []

# Ricostruzione per diversi valori del parametro di regolarizzazione
for i, L in enumerate(lambdas):
    # Esegui la minimizzazione con al massimo 50 iterazioni
    max_iter = 50
    res = minimize(f, x0, (L), method='CG', jac=df, options={'maxiter':max_iter})

    # Aggiungi la ricostruzione nella lista images
    X_curr = res.x.reshape(X.shape)
    images.append(X_curr)

    # Stampa il PSNR e l'mse per il valore di lambda attuale
    PSNR = metrics.peak_signal_noise_ratio(X, X_curr)
    mse = metrics.mean_squared_error(X, X_curr)

    PSNRs.append(PSNR)
    mses.append(mse)
    print(f'PSNR: {PSNR:.3f} (\u03BB = {L})')
    print(f'MSE: {mse:.3f} (\u03BB = {L})')
    print('\n')
    

# Visualizziamo i risultati
plt.figure(figsize=(12, 4))
plt.subplot(121)
plt.plot(lambdas,PSNRs, '-*')
plt.title('PSNR per $\lambda$')
plt.ylabel("PSNR")
plt.xlabel('$\lambda$')


plt.subplot(122)
plt.plot(lambdas,mses, '-m*')
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



# Questo codice implementa una ricostruzione di immagine utilizzando la minimizzazione di una funzione obiettivo. L'immagine originale viene sfocata con un kernel gaussiano, successivamente vengono aggiunti rumore e poi si tenta di ricostruire l'immagine originale minimizzando una funzione obiettivo.

# Ecco una breve panoramica del codice:

# Preparazione dei dati:
# Viene utilizzata un'immagine in scala di grigi presa dal modulo data di skimage e sfocata con un kernel gaussiano.
# Viene aggiunto del rumore gaussiano per simulare un'immagine corrotta.
# Minimizzazione senza regolarizzazione:
# La prima parte del codice implementa una soluzione naive senza regolarizzazione. Viene utilizzata la libreria scipy.optimize per minimizzare la funzione obiettivo.
# Viene tracciato il PSNR e l'MSE per ogni iterazione.
# Minimizzazione con regolarizzazione (Total Variation):
# La seconda parte del codice implementa la regolarizzazione della ricostruzione utilizzando la variazione totale (Total Variation).
# La funzione obiettivo include un termine di regolarizzazione basato sulla variazione totale dell'immagine.
# Vengono tracciati i PSNR e gli MSE per diverse intensità di regolarizzazione.
# Visualizzazione dei risultati:
# Vengono visualizzati il PSNR e l'MSE in funzione dei diversi parametri di regolarizzazione.
# Le immagini originali, corrotte e ricostruite sono visualizzate per confrontare i risultati ottenuti con diversi valori di regolarizzazione.
# Il codice utilizza funzioni di supporto da un modulo utils_SR che probabilmente contiene le definizioni di alcune funzioni necessarie per la minimizzazione e la regolarizzazione.

# In generale, il codice esegue una ricostruzione di immagini sfocate e corrotte, esplorando l'uso di regolarizzazione per ottenere risultati migliori.