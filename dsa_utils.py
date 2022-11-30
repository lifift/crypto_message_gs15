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
    L= 2048
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

    #TEMP
    message=1

    while sign1==0 or sign2==0 : 
        k = random.randrange( 1, q-1 )
        sign1 = pow(g, k, p) % q # The first part of the DSA signature
        sign2 = ( pow(k, -1, q) * (message+x*sign1) ) % q # The second part of the DSA signature
        w = pow(sign2, -1, q)
    return (sign1, sign2)

def verify_sign(message, sign1, sign2, pub_key, p , g):

    #TEMP
    message=1

    w = pow(sign2, -1, q)
    u1 = (message * w) % q
    u2 = (sign1 * w) % q
    
    v =  (pow(g,u1,p) * pow(pub_key,u2,p)%p) % q 
    return ( v==sign1 )



if __name__=="__main__":
    p=25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741
    q=10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221
    #p=451425837041 
    #q=797 
    ( p, q, g, y, x ) =  generate_params(p,q)
    print("x: ",x,"\ny: ",y)
    ( sign1,sign2 )   =  generate_sign(2**256,p,q,g,x)
    #print(sign1,sign2)
    print(verify_sign(2**256, sign1, sign2, y, p , g ))
    