from dsa_utils import verify_sign
from key_creator import key_creator
from hkdf import hkdf
#fonction pour calculer le secret partager de deux clés celon diffie hellman
p = 25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741
q = 10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221
g = 14748285547860891233975997283077896907274400627046553753871151539760884885790168770829593892286143788048038301808860984103407433451119851391335466994980962394563526010784734563078391127116421220207367149688383988307093109855172777250534791066626891030710091026645430537791647762417763540763689690526440459128783520536341692638386402962887016857565951133331589372599887152470297628892163589782630338295530373831428798459219417766656522045003583428041898104475209147065612429325294837587314646241597378875734664388392084098537237428914831710058388398951969618394996838649802283815434179994810830210881507594620419122191
def dh(priv=int(), pub=int()):
    return (pow(pub,priv,p))  #La partie publique puissance partie privé modulo p notre contexte.

def x3dh_send(receiver:str,my_id_priv:int) : # partie initiale de l'échange x3dh (la partie de l'émetteur)
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
    verified = verify_sign(preS_key, signature.split(":")[0], signature.split(":")[1], id_pub, p, g,q)
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
    root_key    = int.from_bytes(derived_keys[:int(len(derived_keys))//2],"little")
    session_key = int.from_bytes(derived_keys[int(len(derived_keys))//2:],"little")


    #return
    return (root_key,id_pub,session_key,num_otPK,eph_pub)



def x3dh_receive(personnal_keys:str,receiver:str,keys:str,my_id_priv:int,my_pre_priv:int) : # partie secondaire de l'échange x3dh (la partie de la reception)
    # return (root_key,id_pub,session_key,num_otPK,eph_pub) 
    server_key_path = "server.keys"
    server_msg_path = "server.msg"
    
    num_otPK     = keys.split(":")[0]
    sender_id_pub= int(keys.split(":")[1])
    eph_pub      = int(keys.split(":")[2]) #public part of the used ephemeral key
    otPK_priv    = 0
    pre_priv     = my_pre_priv
     



    # Récupération/suppression? du bundle de clé en local
    with open(personnal_keys,'r') as f :#FORMAT:name,type,number,private part,public part
        for line in f.readlines():
            try:
                if (line.strip("\n").split(',')[0] == receiver) and (line.split(',')[1] == "otPK") and (line.split(',')[2] == num_otPK): # on cherche la ligne correspond à notre otPK
                    otPK_priv = line.strip("\n").split(',')[3]
            except :
                pass

    if not otPK_priv :
        input("Problème x3dh receive : on n'a pas retrouvé l'otPK")


    #calcul DH 1-4
    """
    1. DH1 = DH(IDprivB ; SigP KpubA ) 
    2. DH2 = DH(EphprivB ; IDpubA ) 
    3. DH3 = DH(EphprivB ; SigP KpubA ) 
    4. DH4 = DH(EphprivB ; OtP KnpubA ) 
    """
    DH1 = dh( int(my_pre_priv) , sender_id_pub )
    DH2 = dh( int(my_id_priv ) , eph_pub )
    DH3 = dh( int(my_pre_priv) , eph_pub )
    DH4 = dh( int(otPK_priv  ) , eph_pub )
    conc_DH = int(str(DH1) +str(DH2) +str(DH3) +str(DH4)) 


    #ratchet initial ?
    length = 4096
    derived_keys = hkdf( 
        length=length, # on prend une longueur de 4096 pour se fournir 2 clés de 2048 bits
        key= conc_DH,
        salt=2**511,
        ) 
    root_key    = int.from_bytes(derived_keys[:int(len(derived_keys))//2],"little")
    session_key = int.from_bytes(derived_keys[int(len(derived_keys))//2:],"little")


    #return
    return (root_key,session_key)


    