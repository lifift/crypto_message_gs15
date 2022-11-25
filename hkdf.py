#SOURCE : https://en.wikipedia.org/wiki/HKDF


import hashlib
import hmac
from math import ceil

hash_len = 512


def hmac_sha512(key, data): #  Besoin d'une fonction de hashage + le HMAC qui prend en charge un sel :'(
    o=hmac.new(key,data, hashlib.sha512)
    output=o.digest()
    return output


def hkdf(length: int,key, salt: bytes = b"") -> bytes:
    """Key derivation function"""
    if len(salt) == 0:
        salt = bytes([0] * hash_len)
    #hashed = hmac_sha512(salt,key)
    hashed = hashlib.sha512(key).digest()
    t = b""
    output = b""
    for i in range(ceil(length / hash_len)): #ceil() c'est un aroundi
        #t = hmac_sha512(hashed, t + bytes([i + 1])) #si on ne fait pas de fonction hmac on pourrait remplacer par  : hashed+t+bytes([i + 1])
        t = hashlib.sha512(hashed+t+bytes([i + 1])).digest() #VERSION SANS HMAC...
        output += t
    return output[:length]
if __name__=='__main__':
    K=bytes.fromhex('0a'*3000) #des bytes attention 
    print (len(K))

    okm = hkdf( length=4096, # on prend une longueur de 4096 pour se fournir 2 clés de 2048 bits
            key=K,
            salt=bytes.fromhex(''),
            )

    print(int.from_bytes(okm, 'little'))
    print(len(okm))