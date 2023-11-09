import numpy as np
import time
import sys
USE_PIL = True
try:
    from PIL import Image
except ImportError:
    USE_PIL = False

SAUVE_IMAGE = 1

rang = 1 # Degré de voisinage

if (len(sys.argv) > 1) : rang = int(sys.argv[1])
mask = 1 << np.arange(2*rang+1)[::-1]

nbCases = 2**(2**rang+1)
dim     = 255
if (len(sys.argv) > 2) : dim = int(sys.argv[2])
nbIters = dim
if (len(sys.argv) > 3) : nbIters = int(sys.argv[3])

print(f"Resume des parametres : ", flush=True)
print(f"\tNombre de cellules : {dim}")
print(f"\tNombre d'iterations : {nbIters}")
print(f"\tDegre de voisinage : {rang}")
print(f"\tNombre de cas à traiter : {2**nbCases}")

chronoCalcul = 0.
chronoPNG    = 0.
for numConfig in range(2**nbCases):
    # Calcul générations
    start = time.time()
    nbCells = dim + 2*rang
    cells = np.zeros((nbIters, nbCells), dtype=np.int8)
    cells[0,nbCells//2] = 1
    for iter in range(1,nbIters):
        cells[iter, rang:-rang] = np.array([1 if (1<< cells[iter-1, i-rang:i+rang+1].dot(mask)) & numConfig else 0 for i in range(rang, dim+rang)], dtype=np.int8)
    chronoCalcul += time.time()-start
    # Sauvegarde image
    if SAUVE_IMAGE:
        if USE_PIL:
            start = time.time()
            img = Image.fromarray((cells * 255).astype(np.uint8))
            img.save(f"config{numConfig:04}.png")
            chronoPNG += time.time() - start
        else:
            start = time.time()
            np.savetxt(f"config{numConfig:04}.txt", cells)
            chronoPNG += time.time() - start

print(f"Temps mis pour le calcul : {chronoCalcul}")
print(f"Temps mis pour sauvegarder l'image : {chronoPNG}")
