" 4. Compressione di un'immagine tramite SVD "

import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
from skimage import data # libreria che permette di caricare/salvare immagini
#from skimage.io import imread

A = data.horse()

#print(type(A)) # stampa il tipo di dato rappresentato dalla vaiabile A
print(A.shape)


U, s, Vh = scipy.linalg.svd(A) # funzione che calcola la SVD di A

A_p = np.zeros(A.shape) # matrice con le stesse dimensioni di A, inizializzata con tutti zeri
# sarà utilizzata per la costruzione di una versione approssimata di A tramite la SVD

plt.figure(figsize=(20, 10)) # crea una figura di dimensioni 20x10
plt.imshow(A, cmap='gray') # Visualizza l'immagine rappresentata dalla matrice A in scala di grigi
plt.title('Immagine originale')
plt.show()


p_max = 100 # numero di addendi della sommatoria; iterazioni utilizzate per approssimare man mano l'immagine 
err_rel = np.zeros((p_max-1)) # array di dimensione (p_max-1,) con gli elementi inizializzati a zero; sarà utilizzato per memorizzare errori relativi
c = np.zeros((p_max-1)) # idem, ma utilizzato per memorizzare i fattori di compressione

for i in range(p_max-1): # grafico del fattore di compressione per p che va da 1 a 99
  ui = U[:, i] # estrae la i-esima colonna da U (autovettori sinistri associati ai valori singolari); fa parte del processo di ricostruzione approssimata della matrice A
  vi = Vh[i, :] #  estrae la i-esima riga da V (autovettori destri associati ai valori singolari)

  A_p = A_p + s[i]*np.outer(ui, vi) # aggiorna la matrice approssimata A_p  sommando il prodotto degli autovettori sx e dx moltiplicato al valore singolare corrispondente
  err_rel[i] = np.linalg.norm(A-A_p, "fro")/np.linalg.norm(A, "fro") # calcola e memorizza l'errore relativo tra A e A_p 
  c[i] = (1/(i+1) * np.min(A.shape))-1 # calcola e memorizza il fattore di compressione in funzione del numero di componenti singolari considerate. Diminuisce all'aumentare del numero di componenti singolari, rappresentando quanto compresso è il dato rispetto alla sua dimensione originale


for i in range(10, 120, 20): # immagini al variare di p
     A_p = np.matrix(U[:,:i])*np.diag(s[:i])*np.matrix(Vh[:i,:]) # esegue la ricostruzione approssimata di A utilizzando un numero specifico i di componenti singolari dalla SVD. np.matrix converte U, Sigma, V in matrici.
     # Durante ogni iterazione vengono utilizzate le prime i componenti singolari per approssimare la matrice originale 
     # A. Viene quindi calcolata la matrice approssimata A_p utilizzando U, sigma, V della decomposizione SVD
     plt.imshow(A_p, cmap='gray')
     plt.title('Immagine ricostruita con p =' + str(i)) # str(i) converte il valore di i (ovvero il numero di componenti singolari utilizzate) in una stringa
     plt.show()

plt.figure(figsize=(10, 5))
fig1 = plt.subplot(1, 2, 1)
fig1.plot(err_rel, 'm-*')
plt.title('Errore relativo') 
fig2 = plt.subplot(1, 2, 2)
fig2.plot(c, 'm-*')
plt.title('Fattore di compressione')
plt.show()

print('\nL\'errore relativo della ricostruzione di A è =', err_rel[-1]) #err_rel[-1] rappresenta l'ultimo valore dell'array err_rel (calcolato durante il ciclo per diverse quantità di componenti singolari); misura l'accuratezza dell'approssimazione rispetto alla matrice originale
print('Il fattore di compressione è =', c[-1]) # c[-1] rappresenta l'ultimo valore dell'array c; misura quanto è stata compressa la matrice rispetto alle sue dimensioni originali, considerando il numero di componenti singolari utilizzate.



# Viene caricata un'immagine utilizzando il modulo skimage.data.

# Viene eseguita la SVD dell'immagine.
# L'SVD scompone l'immagine originale A nei suoi componenti principali U, SIGMA, V.T

# L'immagine originale viene ricostruita utilizzando un numero variabile di p.
# L'obiettivo è studiare come la qualità della ricostruzione e il fattore di
# compressione variano al variare di p.

# Vengono creati due grafici: il primo motra come l'errore relativo di ricostruzione
# varia al variare di p, mentre il secondo mostra come il fattore di compressione
# varia al variare di p.

# Vengono visualizzate le immagini ricostruite al variare di p, permettendo di
# osservare come la qualità della ricostruzione cambi.

