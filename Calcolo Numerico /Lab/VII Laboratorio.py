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
k = gaussian_kernel(24, 3)
plt.imshow(k)
plt.show()

# Blur with FFT
K = psf_fft(k, 24, X.shape)
plt.imshow(np.abs(K))
plt.show()

X_blurred = A(X, K, sf)
plt.subplot(121).imshow(X, cmap='gray', vmin=0, vmax=1)
plt.title('Original')
plt.xticks([]), plt.yticks([])
plt.subplot(122).imshow(X_blurred, cmap='gray', vmin=0, vmax=1) #vmin e vmax indicano i range che vogliamo nel plot
plt.title('Downsampled')
plt.xticks([]), plt.yticks([])
plt.show()

# Blur with openCV
# X_blurred = cv.filter2D(X, -1, k)
# plt.subplot(121).imshow(X, cmap='gray', vmin=0, vmax=1)
# plt.title('Original')
# plt.xticks([]), plt.yticks([])
# plt.subplot(122).imshow(X_blurred, cmap='gray', vmin=0, vmax=1) #vmin e vmax indicano i range che vogliamo nel plot
# plt.title('Downsampled')
# plt.xticks([]), plt.yticks([])
# plt.show()


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
plt.title(f'Corrupted (PSNR: {PSNR:.2f})')
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
for k, x_k in enumerate(res.allvecs):
    PSNR[k] = metrics.peak_signal_noise_ratio(X, x_k.reshape(X.shape))

# Risultato della minimizzazione
X_res = res.x.reshape((m, n))

# PSNR dell'immagine corrotta rispetto all'oginale
starting_PSNR = np.full(PSNR.shape[0], metrics.peak_signal_noise_ratio(X, ATy))

# Visualizziamo i risultati
ax2 = plt.subplot(1, 2, 1)
ax2.plot(PSNR, label="Soluzione naive")
ax2.plot(starting_PSNR, label="Immagine corrotta")
plt.legend()
plt.title('PSNR per iterazione')
plt.ylabel("PSNR")
plt.xlabel('itr')
plt.subplot(1, 2,2).imshow(X_res, cmap='gray', vmin=0, vmax=1)
plt.title('Immagine Ricostruita')
plt.xticks([]), plt.yticks([])
plt.show()

# Regolarizzazione
# Funzione da minimizzare
def f(x, L):
   # nsq = np.sum(np.square(x))
    x  = x.reshape((m, n))
    nsq = totvar(x) #aggiunto; esercizio facoltativo
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
lambdas = [0.01,0.03,0.04, 0.06]
#lambdas = [0.02,0.021,0.022, 0.028] #devo sceglierli io??????????
PSNRs = []
images = []

# Ricostruzione per diversi valori del parametro di regolarizzazione
for i, L in enumerate(lambdas):
    # Esegui la minimizzazione con al massimo 50 iterazioni
    max_iter = 50
    res = minimize(f, x0, (L), method='CG', jac=df, options={'maxiter':max_iter})

    # Aggiungi la ricostruzione nella lista images
    X_curr = res.x.reshape(X.shape)
    images.append(X_curr)

    # Stampa il PSNR per il valore di lambda attuale
    PSNR = metrics.peak_signal_noise_ratio(X, X_curr)
    PSNRs.append(PSNR)
    print(f'PSNR: {PSNR:.2f} (\u03BB = {L:.2f})')
    
    

# Visualizziamo i risultati
plt.plot(lambdas,PSNRs)
plt.title('PSNR per $\lambda$')
plt.ylabel("PSNR")
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
  plt.title(f"Ricostruzione ($\lambda$ = {L:.2f})")
plt.show()


#da scrivere nella console
#plt.imshow(X)
#plt.imshow(noise, cmap = "gray")
#plt.imshow(y, cmap = "gray")