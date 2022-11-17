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

def generate_params(p,q):
    L= 3072
    N = 512
    z = (p-1) // q
    #print(z)
    h = 1
    g = 0
    while g<=1 :
        h+=1
        g = pow(h, z, p)
    x = random.randrange(p>>1, p ) # partie privé de la clé. Un entier aléatoire de l'orde de grandeur de q
    ## TODO  peut on remplacer x par une clé privé de 2048 bit ?????
    y = pow(g, x, p) # partie publique de la clé
    return ( p, q, g, y, x )

def generate_sign(message, p, q, g, x):
    sign1 = 0
    while sign1==0 or sign2==0 : 
        k = random.randrange( 1, q-1 )
        sign1 = pow(g, k, p) % q # The first part of the DSA signature
        sign2 = ( pow(k, -1, q) * (message+x*sign1) ) % q # The second part of the DSA signature
        w = pow(sign2, -1, q)
    return (sign1, sign2)

def verify_sign(message, sign1, sign2, pub_key, p , g):
    w = pow(sign2, -1, q)
    u1 = (message * w) % q
    u2 = (sign1 * w) % q
    
    v =  (pow(g,u1,p) * pow(pub_key,u2,p)%p) % q 
    return ( v==sign1 )



if __name__=="__main__":
    p=42319497670192821545946615252209673109677225028613892412561386782526930920583767194139955881001195614668775056120404415013148090951892954204953909865916795037269938465835747093967448520123816629302706544939395131405659753939183809402981935857266275419317363356979266075303232855495809448782012453565615220666359358597692203498934195533397118957309475530089462348663140647771188572603816330556171310194843968069269597715463407705438237909279601180783489982448491361578170614483778384033872254117814346539879827151387383182980444307667080622689463771297923414369153073665931997870285588226267462998861424143849380040760062189397904328901233915250848860200442291669324552424156186921362931705560674921077997437286080141422507991846514280479735357586258220163014074338615507450563623709715452897143169784539524624496307339027346522137698586918638418412741868881039059232376594450944027944747638311678179270400393304330239805571567
    q=6987996590433036289133966107502273878194324094372457338088403547531577896701394141824845328358861006000565922233052113753739754313712307851443210692660973
    #p=451425837041 
    #q=797 
    ( p, q, g, y, x ) =  generate_params(p,q)
    print("x: ",x,"\ny: ",y)
    ( sign1,sign2 )   =  generate_sign(2**256,p,q,g,x)
    #print(sign1,sign2)
    print(verify_sign(2**256, sign1, sign2, y, p , g ))
    