import numpy as np
import matplotlib.pyplot as plt
import scipy.linalg
from skimage import data
from skimage.io import imread

# help(data)

A = data.coffee()
#A = imread('phantom.png') 
A=A[:, :, 0] #selezione di un pezzo di matrice da un tensore

print(type(A))
print(A.shape)


plt.imshow(A, cmap = "gray")
plt.show()


U, s, Vh = scipy.linalg.svd(A) #calcola la fattorizzazione svd

print('\nShape of U:', U.shape)
print('Shape of s:', s.shape)
print('Shape of V:', Vh.T.shape)

A_p = np.zeros(A.shape) #crea una matrice di dimensione A
p_max = 10 #rango di apprssimazione immagine
#np.min(A.shape) comando ottimale per far vedere l'immagine


for i in range(p_max):
  ui = U[:, i]
  vi = Vh[i, :]

  A_p = A_p + s[i]*np.outer(ui, vi) #sommatoria


err_rel = np.linalg.norm(A-A_p, 2)/np.linalg.norm(A,2)
c = (1/p_max*np.min(A.shape))-1

print('\n')
print('L\'errore relativo della ricostruzione di A è', err_rel)
print('Il fattore di compressione è c=', c)


plt.figure(figsize=(20, 10))

fig1 = plt.subplot(1, 2, 1)
fig1.imshow(A, cmap='gray')
plt.title('True image')

fig2 = plt.subplot(1, 2, 2)
fig2.imshow(A_p, cmap='gray')
plt.title('Reconstructed image with p =' + str(p_max))

plt.show()



# al variare di p
p_max = 100
A_p = np.zeros(A.shape)
err_rel = np.zeros((p_max))
c = np.zeros((p_max))

for i in range(p_max):
  ui = U[:, i]
  vi = Vh[i, :]

  A_p = A_p + s[i]*np.outer(ui, vi)
  err_rel[i] = np.linalg.norm(A-A_p, "fro")/np.linalg.norm(A, "fro") #ogni iterazione calcolo l'errore e il fattore di compressione rispetto all'elemento p del for
  c[i] = (1/(i+1) * np.min(A.shape))-1 #fattore di compressione rispetto all'elemtno p


plt.figure(figsize=(10, 5))

fig1 = plt.subplot(1, 2, 1)
fig1.plot(err_rel, 'm-*')
plt.title('Errore relativo') 

fig2 = plt.subplot(1, 2, 2)
fig2.plot(c, 'm-*')
plt.title('Fattore di compressione') #man mano aumento p la compressione diminuisce fino a tendere a zero (minimo delle dimensioni della matrice )

plt.show()