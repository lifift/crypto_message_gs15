#SOURCE : https://en.wikipedia.org/wiki/HKDF


import hashlib
import hmac
from math import ceil
from eponge import hash512

hash_len = 512


def hmac_sha512(key, data): #  Besoin d'une fonction de hashage + le HMAC qui prend en charge un sel :'(
    o=hmac.new(key,data, hashlib.sha512)
    output=o.digest()
    return output

# on modifie un peu la fonction pour se rapprocher de HKDF1 et donc ne pas avoir à utiliser un HMAC
def hkdf(length= int(),key= int(), salt= int()) -> bytes:
    """Key derivation function"""
    xored = int.to_bytes(key^salt,2000,'little')
    if salt == 0:
        salt = bytes([0] * hash_len)
    else : 
        salt = int.to_bytes(salt,2000,'little') #le 2049 bytes est bizard mais bon ....
    key = int.to_bytes(key,2000,'little')
    #hashed = hmac_sha512(salt,key)
    hashed = int.to_bytes(hash512(xored),64,'little')
    t = b""
    output = b""
    for i in range(ceil(length / hash_len)): #ceil() c'est un aroundi
        #t = hmac_sha512(hashed, t + bytes([i + 1])) #si on ne fait pas de fonction hmac on pourrait remplacer par  : hashed+t+bytes([i + 1])
        t = int.to_bytes(hash512(hashed+t+bytes([i + 1])),64,'little') #VERSION SANS HMAC...
        output += t
    return output[:length]


if __name__=='__main__':
    import random
    K=int.to_bytes((2**2048)-7896,512,'little') #des bytes attention
    K=int.to_bytes(0,512,'little')
    K= bytes("\x00"*1024,"utf-8")
    #print(bin(int.from_bytes(K,'little')))
    #print (len(K))
    print("input material : ",str(K))
    okm = hkdf( length=4096, # on prend une longueur de 4096 pour se fournir 2 clés de 2048 bits
            key=int.from_bytes(K,'little'),
            salt=random.randint(2**2045,2**2048)
            )
    
    print("output material : ",str(okm))
    root_key    = okm[:int((len(okm)/2))]
    session_key = okm[(int(len(okm)/2)):]

    #print(int.from_bytes(okm, 'little'))
    #print( root_key , "   " ,len(session_key))
    #
