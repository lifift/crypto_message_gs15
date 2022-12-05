#SOURCE : https://en.wikipedia.org/wiki/HKDF


import hashlib
import hmac
from math import ceil

hash_len = 512


def hmac_sha512(key, data): #  Besoin d'une fonction de hashage + le HMAC qui prend en charge un sel :'(
    o=hmac.new(key,data, hashlib.sha512)
    output=o.digest()
    return output


def hkdf(length= int(),key= int(), salt= int()) -> bytes:
    """Key derivation function"""
    if salt == 0:
        salt = bytes([0] * hash_len)
    else : 
        salt = int.to_bytes(salt,2049,'little')
    key = int.to_bytes(key,2049,'little')
    hashed = hmac_sha512(salt,key)
    #hashed = hashlib.sha512(key).digest()
    t = b""
    output = b""
    for i in range(ceil(length / hash_len)): #ceil() c'est un aroundi
        t = hmac_sha512(hashed, t + bytes([i + 1])) #si on ne fait pas de fonction hmac on pourrait remplacer par  : hashed+t+bytes([i + 1])
        #t = hashlib.sha512(hashed+t+bytes([i + 1])).digest() #VERSION SANS HMAC...
        output += t
    return output[:length]
if __name__=='__main__':
    K=int.to_bytes((2**2048)-7896,512,'little') #des bytes attention
    #print(bin(int.from_bytes(K,'little')))
    #print (len(K))

    okm = hkdf( length=4096, # on prend une longueur de 4096 pour se fournir 2 clés de 2048 bits
            key=int.from_bytes(K,'little'),
            salt=2**511,
            )
    
    print(len(okm))
    root_key    = okm[:int((len(okm)/2))]
    session_key = okm[(int(len(okm)/2)):]

    #print(int.from_bytes(okm, 'little'))
    print( len(root_key) , "   " ,len(session_key))
    #
