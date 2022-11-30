"""
A function to create a couple private/public key.

This couple depend of the type of key needed : 
    type 1 : ID key for long terme use
    type 2 : preSigned key 
    type 3 : one time use key 
    type 4 ephemeral key
"""
try :
    import random
    from modular_power import modular_power
except :
    exit()

# p the prime defining our abelian group
p = 25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741

def key_creator( KeyType:int(), p, g ):


    KeySize = 0  # size of the key in bits
    if   KeyType == 1 : KeySize = 2048
    elif KeyType == 2 : KeySize = 512 # need to talk about this one ? always 2048 ?
    elif KeyType == 3 : KeySize = 512 # same
    else              : KeySize = 512 # same

    priv = random.randrange( 2**(KeySize-1), p ) 

    pub  = modular_power( g, priv, p )

    return (priv,pub)

if __name__ == '__main__': 
    (x,y) = key_creator( 1 , p=p, g=2 )
    print ( "clé privé : "+str(x)+ "\nclé publique : "+str(y) )
    #print (int.to_bytes(x, 2048, 'little'))
