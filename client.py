
import time
import random
from key_creator import key_creator
from dh import diffie_hellman
from dh import x3dh_send
from dh import x3dh_receive
from hkdf import hkdf
from dsa_utils import generate_sign
from dsa_utils import verify_sign

p = 25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741
q = 10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221
g = 2

APP_SALT = 2**511
# selecting a user


def x3dh(target:str): #fait l'échange diffie hellman et retourne les paramètre à enregistrer
    return(0,0,0,0,0) # root_key,id_pub,session_key

def check_msg():# met à jour les messages de "ID" en interrogeant le serveur
    with open(server_msg_path,'r') as f : 
        lines = f.readlines()
    new_msg = []
    with open(server_msg_path, "w") as f:
        for line in lines:
            try : 
                if line.strip("\n").split(',')[1] != myID: #format d'une ligne : origin,dest,id,date,data,?type?,...
                    f.write(line)
                else :
                    new_msg.append(line.strip("\n"))
            except : 
                pass
    print(str(len(new_msg))," nouveaux messages !")
    for x in new_msg :
        read_msg(x) # READ_MSG une fonction à créer qui traite les messages en fonction de leur type : message, init , ack, fichier
        
def check_conv(friend=str(),mode=int()):
    with open(personnal_msg,'r') as f : 
        lines = f.readlines() #format d'une ligne locale : sender, receiver, id, ack, date, msg  
    inbox  = []
    outbox = []
    for line in lines :
        try :
            sender   = line.split(',')[0]
            receiver = line.split(',')[1]
            ack      = line.split(',')[3]
            date     = line.split(',')[4]
            msg      = line.split(',')[5] # On stocke le message en clair mais on ne stocke pas la clé
        
            if (sender==friend) or (receiver==friend) :
                output= ""
                if ack == "True":
                    output += 'x '
                else :
                    output += 'o '
                
                if mode == 0:#mode print
                    output += date + "\n" + sender + ' => ' + receiver + " # " + msg # x 24 novembre 2020 \n Bob => Alice # Il fait très beau demain :) 
                    print (output)
                else :
                    return (output)
        except :
            pass

def read_msg(message=str()):
    #FORMAT : origin,dest,id,date,data,type,keys,signature
    sender   = message.split(',')[0]
    receiver = message.split(',')[1]
    msg_id   = message.split(',')[2] # id  aléatoire, random+hash du message ?
    date     = message.split(',')[3]
    data     = message.split(',')[4]
    msg_type = message.split(',')[5]
    keys     = message.split(',')[6]
    signature= message.split(',')[7]

    if msg_type == "ACK": # le message recu est un accusé de reception
        with open(personnal_msg,'r') as f : 
            lines = f.readlines()
        with open(personnal_msg, "w") as f:
            for line in lines:
                try :
                    if line.strip("\n").split(',')[2] != msg_id: # on retrouve le message dont on recoit l'acquittement
                        f.write(line)
                    else :
                        f.write(line.replace(msg_id+",False",msg_id+",True"))
                except :
                    pass

    if msg_type == "INIT": #besoin d'un init ? 
        #FORMAT : origin,dest,id,date,data,type,keys,signature

        sender_id_pub = keys.split(":")[1]

        #faire le x3dh
        (root_key,session_key)=x3dh_receive(personnal_keys, myID, keys, my_id_priv, my_pre_priv)

        # HKDF session => (session+comm_key) 
        x = hkdf(4096,session_key,APP_SALT)
        (session_key,comm_key) = (int.from_bytes(x[:2048],'little'),int.from_bytes(x[2048:],'little')) 

        #vérifier une signature ?
        verified = verify_sign(data, signature.split(":")[0], signature.split(":")[1], sender_id_pub, p, g)
        if not verified :
            print("HACKER")
            return


        #Stocker les clé pour le futur
        payload = sender+","+str(root_key)+","+sender_id_pub+","+str(session_key)+"\n"# FORMAT : name,root_key, his public id, the session last key
        with open(personnal_keys,'a') as f : 
            f.write(payload)

        # déchiffrer le message.
        # stocker le message en local
        with open(personnal_msg,'a') as f:
            output = "\n"+sender+","+receiver+","+ msg_id+","+"True"+","+date+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)
    
    if msg_type == "FILE":
        

        # envoyer un ACK pour ce message
        with open(server_msg_path,'a') as f : # ouverture en mode "append" pour stocker notre  ACK sur le serveur
            output = "\n"+myID+","+sender+","+ msg_id+","+date.date+",ACK,ACK" 
            f.write(output)

        #FORMAT : origin,dest,id,date,data,type,keys,signature

        # aller chercher la clé du ratchet de cette conv,
        #  faire un tours de moulinnette pour avoir la clé de déchiffrement, et du prochain ratchet 
        # stocker la nouvelle clé de ratchet
        # déchiffrer le fichier.
        # stocker le fichier dans le dossier files avec un nom parlant => id.sender.receiver 



    if msg_type == "MSG": 

        # envoyer un ACK pour ce message
        with open(server_msg_path,'a') as f : # ouverture en mode "append" pour stocker notre  ACK sur le serveur
            output = "\n"+myID+","+sender+","+ msg_id+","+"date.date"+",ACK,ACK" #origin,dest,id,date,data=ACK,type=ACK
            f.write(output)
        

        #FORMAT : origin,dest,id,date,data,type,keys,signature
        # aller chercher la clé du ratchet de cette conv,
        with open (personnal_keys,'r') as f : # ici on essaie de chopper les valeurs du ratchet précédent si elles existent 
            for line in f.readlines():
                if line.split(",")[0] == receiver : # FORMAT : name,root_key, his public id, the session last key
                    root_key      = int(line.split(",")[1]) # aller retrouver la root_key actuelle
                    sender_id_pub = int(line.split(",")[2]) # retrouver l'ID publique de l'autre 
                    session_key   = int(line.split(",")[3]) # retrouver le dernier secret partagé utilisé 
       
        num_otPK     = keys.split(":")[0]
        sender_id_pub= int(keys.split(":")[1])
        eph_pub      = keys.split(":")[2]
        # Check if it is a new session
        new_session = True
        if eph_pub=="NONE":
            new_session = False

        if new_session :
            #  faire un tours de moulinnette pour avoir la clé de déchiffrement, et du prochain ratchet 
            shared_key = diffie_hellman(my_id_priv,int(eph_pub)) 

            # Premier HKDF
            x = hkdf(4096,root_key,shared_key)#on fait le hkdf ave la shared_key 
            root_key = int.from_bytes(x[:2048],'little')
            session_key = int.from_bytes(x[2048:],'little')

            # Second HKDF
            x = hkdf(4096,session_key,APP_SALT)
            session_key = int.from_bytes(x[:2048],'little')
            comm_key = int.from_bytes(x[2048:],'little')
        
        if not new_session : #on ne fait que le second hkdf si on ne change pas de session
            # Second HKDF
            x = hkdf(4096,session_key,APP_SALT)
            session_key = int.from_bytes(x[:2048],'little')
            comm_key = int.from_bytes(x[2048:],'little')



        #Stocker les clé pour le futur
        payload = sender+","+str(root_key)+","+sender_id_pub+","+str(session_key)+"\n"# FORMAT : name,root_key, his public id, the session last key
        with open(personnal_keys,'r') as f : 
            lines = f.readlines()
        with open(personnal_keys,'w') as f : 
            for line in lines :
                try:
                    if line.split(",")[0] == sender :
                        f.write(payload)
                    else :
                        f.write(line)
                except:pass

        # déchiffrer le message.
        # stocker le message en local
        with open(personnal_msg,'a') as f:
            output = "\n"+sender+","+receiver+","+ msg_id+","+"True"+","+date+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)














def send_msg():#chiffrer / ratchet et tout et tout 
    receiver =  input("Pour qui est votre message ? : ")

    #TEST existance ? => clés sur le serveurs ?
    exist = False
    with open(server_key_path,'r') as f :
        for line in f.readlines() :
            if line.split(",")[0] == receiver :
                exist = True
    if not exist:
        print (receiver+" n'existe pas.\n\n")
        time.sleep(2)
        return #on quitte la fonction et on retourne au menu principal


    data = input("Entrez votre message : ")
    keys = ""

    # PREMIER MESSAGE ? && Tester si le dernier message a été acquitté
    init_message = False
    new_eph = True #A-t-on besoin d'une nouvelle clé ephemere ?
    conv = check_conv(receiver,1)#on stocke les valeurs d'acquittement actuelle. Des x ou des o
    if conv is None : #si la conversation est vide, on doit faire x3dh echange de clés et tofu
        init_message = True
    

    elif "o" in conv :
        new_eph = False # Il y a un message non acquitté, donc on reste sur la même session (peut-être)
    
    # START DOUBLE RATCHET
    with open (personnal_keys,'r') as f : # ici on essaie de chopper les valeurs du ratchet précédent si elles existent 
        for line in f.readlines():
            if line.split(",")[0] == receiver : # FORMAT : name,root_key, his public id, the session last key
                root_key    = int(line.split(",")[1]) # aller retrouver la root_key actuelle
                id_pub      = int(line.split(",")[2]) # retrouver l'ID publique de l'autre 
                session_key = int(line.split(",")[3]) # retrouver le dernier secret partagé utilisé 



    
    if init_message :
        # X3DH si premier message ............
        (root_key,id_pub,session_key,num_otPK,eph_pub) = x3dh_send(receiver,my_id_priv) #TODO  aie aie aie aie aie aiea aie
        keys += str(num_otPK)+":"+str(my_id_pub)+":"+str(eph_pub)
        #Le HKDF sur la root_key est effectué dans le x3dh (je crois)
        x = hkdf(4096,session_key,APP_SALT)
        session_key = int.from_bytes(x[:2048],'little')
        comm_key = int.from_bytes(x[2048:],'little')

    # END DOUBLE RATCHET

    if not init_message :

        keys += "NONE:"+str(my_id_pub)+":"
        if not new_eph :#si on garde notre session on ne met que la session key à jour 
            x = hkdf(4096,session_key,APP_SALT)
            session_key = int.from_bytes(x[:2048],'little')
            comm_key = int.from_bytes(x[2048:],'little') #Enfin on a la clé de chiffrement du message 

            #tricks pour rester dans la même session, on n'envoie pas de key sur le deuxième message
            keys+="NONE"

        if new_eph:
            #création d'une clé ephemère 
            (eph_priv,eph_pub) = key_creator(4,p,g) # Création d'un clé éphémère 
            #calcul de la clé partagée correspondante
            shared_key = diffie_hellman(eph_priv,id_pub) 

            #on envoie la partie publique de notre clé ephemère
            keys += str(eph_pub) 

            # Premier HKDF
            x = hkdf(4096,root_key,shared_key)#on fait le hkdf ave la shared_key 
            root_key = int.from_bytes(x[:2048],'little')
            session_key = int.from_bytes(x[2048:],'little')

            # Second HKDF
            x = hkdf(4096,session_key,APP_SALT)
            session_key = int.from_bytes(x[:2048],'little')
            comm_key = int.from_bytes(x[2048:],'little')

    # MAJ des keys local pour cette conversation

    """
    ATTENTION
    Il faudrait normalement conserver les clés précédantes pendant un petit moment. 
    On ignore le problèmes d'un mauvais ordre d'arrivé des messages pour le moment.
    """
    payload = receiver+","+str(root_key)+","+str(id_pub)+","+str(session_key)+"\n"# FORMAT : name,root_key, his public id, the session last key
    with open(personnal_keys,'r') as f : 
        lines = f.readlines()
    with open(personnal_keys, "w") as f:
        for line in lines:
            try :
                if line.strip("\n").split(',')[0] == receiver: # on retrouve la ligne assigné à notre correspondant
                    f.write(payload)
                else :
                    f.write(line)
            except :
                pass


    
    

    


    # chiffrement



    # Signature 
    (x,y)=generate_sign(data,p,q,g,my_id_priv)
    signature=str(x)+":"+str(y) # on concatène les deux parties de la signature 

    # ID
    msg_id = str(random.randint(10000, 100000))
    # date 
    date = str(int(time.time()))
    # type du message 
    if init_message :
        msg_type = "INIT"
    else :
        msg_type = "MSG"
    # stocker le message sur le serveur
    with open(server_msg_path,'a') as f :

        output = "\n"+myID+","+receiver+","+msg_id+","+date+","+data+","+msg_type+","+keys+","+signature #origin,dest,id,date,data=ACK,type=ACK,keys,signature
        f.write(output)
     # stocker le message en local ATTENTION A mettre le message en clair en local
    with open(personnal_msg,'a') as f:
            output = "\n"+myID+","+receiver+","+ msg_id+","+"False"+","+date+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)




















if __name__=="__main__":
    myID = input("Enter your name : ")
    print(" ##### Bonjour ",myID," ##### ")


    personnal_msg = "personnal_data/"+myID+".msg"
    personnal_keys = "personnal_data/"+myID+".keys"
    server_key_path = "server.keys"
    server_msg_path = "server.msg"
    # Nouvel user ?
    new_user = False
    try :
        with open(personnal_msg,'r')as f:
            pass
    except :
        new_user = True


    # generation et de clés
    if new_user :
        with open(personnal_msg,'a')as f:#création des files
            pass
        with open(personnal_keys,'a')as f:
            pass
        (my_id_priv,my_id_pub) = key_creator(1, p, g) #ID KEY
        (my_pre_priv,my_pre_pub) = key_creator(2, p, g) #PRESIGNED KEY
        file_data = myID+","+"ID"+",1,"+str(my_id_priv)+","+str(my_id_pub) #FORMAT : name,type,number,private part,public part
        file_data += "\n"
        file_data += myID+","+"PRE"+",1,"+str(my_pre_priv)+","+str(my_pre_pub)

        (otPK_priv,otPK_pub) = key_creator(3, p, g) #the first otPK we will send to the serveur
        file_data += "\n"
        file_data += myID+","+"otPK"+","+str(0)+","+str(otPK_priv)+","+str(otPK_pub)
        for i in range (4) :
            (tPK_priv,tPK_pub) = key_creator(3, p, g) # 4 other ONE TIME KEY
            file_data += "\n"
            file_data += myID+","+"otPK"+","+str(i+1)+","+str(tPK_priv)+","+str(tPK_pub)
            

        # stockage et depot des clés
        
        with open(personnal_keys, 'w') as f : #stockage en "local"
            f.write(file_data)
        
        with open(server_key_path, "a") as f :
            (x,y)=generate_sign(my_pre_pub,p,q,g,my_id_priv) #signature de la preSIGNED public avec le ID private
            signature=str(x)+":"+str(y) # on concatène les deux parties de la signature 
            payload = myID+","+str(my_id_pub)+","+str(my_pre_pub)+","+str(signature)+",0:"+str(otPK_pub)+"\n" 
            #          name,      ID,               preSIGN,          SIGN(preSIGN),  num:   otPK
            f.write(payload)



    # inititalisation des variables perso
    my_id_priv = 0
    my_id_pub  = 0
    my_pre_priv= 0
    my_pre_pub = 0
    if not(new_user): #on doit récupérer l'id privé et peut être d'autre truc
        with open( personnal_keys, 'r') as f:
            for line  in f.readlines():
                if line.split(',')[0] == myID and line.split(',')[1] == "ID":
                    my_id_priv = int(line.split(',')[3]) #FORMAT : name,type,number,private part,public part
                    my_id_pub = int(line.split(',')[4])
                if line.split(',')[0] == myID and line.split(',')[1] == "PRE":
                    my_pre_priv = int(line.split(',')[3]) #FORMAT : name,type,number,private part,public part
                    my_pre_pub = int(line.split(',')[4])
    


    RUNNING = True
    while RUNNING : 
        action = input("Que voulez vous faire ?\n [r] Raffraichir les messages\n [a] Afficher une conversation\n [e] Envoyer un message\n [q] Quitter\n => ")
        if action == "r":
            check_msg()
        if action == "e":
            send_msg()
        if action == "a" :
            nom = input("Qui ? : ")
            check_conv(nom,0)
        if action == "q" :
            print(" ##### Au revoir ##### ")
            RUNNING = False
        