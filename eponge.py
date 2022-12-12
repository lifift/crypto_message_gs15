#source Wikipédia : https://fr.wikipedia.org/wiki/Fonction_%C3%A9ponge#:~:text=En%20cryptographie%2C%20une%20fonction%20%C3%A9ponge,pour%20la%20fonction%20SHA%2D3.

from shasha import sha3
import numpy as np
import time


# Type      | Output length  | Rate (r)         | Capacity (c)  | F-function input
# SHA3-512  | 512            | 576 bits         | 1024          | 1600
#           | taille du hash | taille de bloc   |
##################################################################################


#fonction de bourrage
def bourrage(flux):

    reste = (len(flux)) % 576

    flux += b'\x00' * (576 - reste) #implémenter le bourrage de sha3 ?

    return flux

#fonction transformation de b bits -> b bits / permutation
def transform(bloc):
    
    return sha3(bloc, False).tolist()


#fonction permettant de convertir des bytes en bits dans un tableau pour chaque éléments
#source stack overflow https://stackoverflow.com/questions/8815592/convert-bytes-to-bits-in-python
def byte2bin(b):
    return [int(X) for X in "".join(["{:0>8}".format(bin(X)[2:])for X in b])]


def absorb(flux):
    etat = [0]*1600 #1600 bits initialisés à 0
    
    nbBlocs = len(flux)//72
    
    for i in range (nbBlocs):

        bloc = (flux[i*72:(i+1)*72]) #nouveau bloc de 72 bytes = 576 bits
        
        bloc = byte2bin(bloc) #conversion des bytes en tableau de bits [1, 0, 0, 1 etc]

        bloc += [0]*1024 #besoin d'avoir la meme taille que etat pour le xor
        
        etat = transform(np.bitwise_xor(etat, bloc)) #calcul du nouvel etat à l'aide de keccak
        
    
    return etat


def essorage(etat):
    z = [] #initialisation de z la sortie*
    while len(z) < 511 :
        z += etat[0:575]
        
        etat = transform(etat)
    return z[0:511]



def hash512(flux:bytes) -> int:
    #a=time.time()
    flux = bourrage(flux)
    #b=time.time()
    flux = absorb(flux)
    #c=time.time()
    hash = essorage(flux)
    #d=time.time()
    hash = eval('0b' + ''.join(str(n) for n in hash))
    #print ("bourrage : ",str(b-a))
    #print ("absorb : ",str(c-b))
    #print ("essorage : ",str(d-c))

    return hash


if __name__=="__main__":
    flux = b'Hello'*100
    #sponge(flux)

    print(hash512(flux))
    #print(sha3([0]*200).tolist())

