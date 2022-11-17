"""
All functions in order to sign and verify a signature using DSA.
Based on : https://fr.wikipedia.org/wiki/Digital_Signature_Algorithm
"""
try :
    import random
    from modular_power import modular_power
    from prime_generator import generate_prime
except :
    exit()

def generate_params(p):
    L= 3072
    N = 512
    q = 0 
    while  (p-1) % q != 0 :
        q = generate_prime( N ) # TODO : tester la longueur de cette opération
    z = p-1 / q

    h = 1
    g = 0
    while g<=1 :
        h+=1
        g = modular_power(h, z, p)
    
    x = random.randrange(q>>1, q ) # partie privé de la clé. Un entier aléatoire de l'orde de grandeur de q
    ## TODO  peut on remplacer x par une clé privé de 2048 bit ?????
    y = modular_power(g, x, p) # partie publique de la clé
    return ( p, q, g, y, x )

def generate_sign(message, p, q, g, x):
    

    sign1 = 0
    while sign1==0 or sign2==0 : 
        s = random.randrange( 1, q )
        sign1 = modular_power(g, s, p) % q # The first part of the DSA signature
        sign2 = ( (1/s) * (H(message)+x*sign1) ) % q # The second part of the DSA signature
    return (sign1, sign2)

def verify_sign(sign1, sign2, pub_key, p , g):
    return True