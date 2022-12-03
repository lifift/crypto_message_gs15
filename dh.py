from dsa_utils import verify_sign
from key_creator import key_creator
from hkdf import hkdf
#fonction pour calculer le secret partager de deux clés celon diffie hellman
p = 25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741
q = 10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221
g = 2
def diffie_hellman(priv=int(), pub=int()):
    return (pow(pub,priv,p))  #La partie publique puissance partie privé modulo p notre contexte.

def x3dh_send(personnal_keys:str,receiver:str,message:str,my_id_priv:int) : # partie initiale de l'échange x3dh (la partie de l'émetteur)
    # return (root_key,id_pub,session_key,num_otPK,eph_pub) 
    server_key_path = "server.keys"
    server_msg_path = "server.msg"

    # Récupération/suppression d'un bundle de clé sur le serveur
    FOUND = False
    with open(server_key_path,'r') as f : #    name,  ID,  preSIGN, SIGN(preSIGN), num:otPK
        lines = f.readlines()
    with open(server_key_path, "w") as f:
        for line in lines:
            try :
                if (line.strip("\n").split(',')[0] == receiver) and not FOUND: # on cherche une ligne correspond à notre destinataire
                    id_pub   = line.split(',')[1] #id publique de notre cible
                    preS_key = line.split(',')[2] #presigned
                    signature= line.split(',')[3]
                    num_otPK = line.split(',')[4].split(':')[0]
                    otPk     = line.split(',')[4].split(':')[1]
                    FOUND = True #on ne prend qu'une ligne 
                else :
                    f.write(line)
            except :
                print(" pb x3dh sender")
                pass
    # verify signature
    verified = verify_sign(message, signature.split(":")[0], signature.split(":")[1], id_pub, p, g)
    if not verified :
        print("HACKER")
        return
    #generate ephemeral key

    (eph_priv,eph_pub) = key_creator(4, p, g)

    #calcul DH 1-4
    """
    1. DH1 = DH(IDprivB ; SigP KpubA ) 
    2. DH2 = DH(EphprivB ; IDpubA ) 
    3. DH3 = DH(EphprivB ; SigP KpubA ) 
    4. DH4 = DH(EphprivB ; OtP KnpubA ) 
    """
    DH1 = dh( my_id_priv,int(preS_key) )
    DH2 = dh( eph_priv,  int(id_pub)   )
    DH3 = dh( eph_priv,  int(preS_key) )
    DH4 = dh( eph_priv,  int(otPk)     )
    conc_DH = int(str(DH1) +str(DH2) +str(DH3) +str(DH4)) 

    #ratchet initial ?
    length = 4096
    derived_keys = hkdf( 
        length=length, # on prend une longueur de 4096 pour se fournir 2 clés de 2048 bits
        key= conc_DH,
        salt=2**511,
        ) 
    root_key    = int.from_bytes(derived_keys[:int(len(derived_keys))/2],"little")
    session_key = int.from_bytes(derived_keys[int(len(derived_keys))/2:],"little")


    #return
    return (root_key,id_pub,session_key,num_otPK,eph_pub)


    