
import time
import random
from key_creator import key_creator
from dh import diffie_hellman
from hkdf import hkdf
from dsa_utils import generate_sign
from dsa_utils import verify_sign

p = 25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741
q = 10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221
g = 2
# selecting a user


# On suppose que les clés sont déja manuellement déposé sur le serveur

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
        
def check_conv(friend=str()):
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
                output += date + "\n" + sender + ' => ' + receiver + " # " + msg # x 24 novembre 2020 \n Bob => Alice # Il fait très beau demain :)
                print (output)
        except :
            pass

def read_msg(message=str()):
    #format d'un message : origin,dest,id,date,data,type
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
    
    if msg_type == "FILE":
        # envoyer un ACK pour ce message
        with open(server_msg_path,'a') as f : # ouverture en mode "append" pour stocker notre  ACK sur le serveur
            output = "\n"+myID+","+sender+","+ msg_id+","+date.date+",ACK,ACK" 
        # aller chercher la clé du ratchet de cette conv,
        #  faire un tours de moulinnette pour avoir la clé de déchiffrement, et du prochain ratchet 
        # stocker la nouvelle clé de ratchet
        # déchiffrer le fichier.
        # stocker le fichier dans le dossier files avec un nom parlant => id.sender.receiver 

    if msg_type == "INIT": #besoin d'un init ? on pourrait stocker le num de otPK dans la var keys ..
        # premier message lors d'un communication
        # On devrait donc avoir plusieurs info dans les datas : clé ephemère, numéro de l'oTPK utilisé
        print("Faire des trucs ... Stocker la clé partagé/chainage dans un fichier")

    if msg_type == "MSG":
        # envoyer un ACK pour ce message
        with open(server_msg_path,'a') as f : # ouverture en mode "append" pour stocker notre  ACK sur le serveur
            output = "\n"+myID+","+sender+","+ msg_id+","+"date.date"+",ACK,ACK" #origin,dest,id,date,data=ACK,type=ACK
            f.write(output)
        # aller chercher la clé du ratchet de cette conv,
        #  faire un tours de moulinnette pour avoir la clé de déchiffrement, et du prochain ratchet 
        # stocker la nouvelle clé de ratchet
        # déchiffrer le message.
        # stocker le message en local
        with open(personnal_msg,'a') as f:
            output = "\n"+sender+","+receiver+","+ msg_id+","+"True"+","+date+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)


def send_msg():#chiffrer / ratchet et tout et tout 
    receiver =  input("Pour qui est votre message ? :  ")

    #TEST existance ? => clés sur le serveurs ?



    data = input("Entrez votre message : ")
    keys = ""

    # PREMIER MESSAGE ? && Tester si le dernier message a été acquitté
    init_message = True
    new_eph = False #A-t-on besoin d'une nouvelle clé ephemere ?
    
    
    # ratchet

    root_key=0 # aller retrouver la root_key actuelle
    id_pub = 0 # retrouver l'ID publique de l'autre 
    session_key = 0 # retrouver le dernier secret partagé utilisé 
    if new_eph :
        (eph_priv,eph_pub) = key_creator(4,p,g) # Création d'un clé éphémère 
        secret = diffie_hellman(eph_priv,id_pub) #le secret partagé pour update le ratchet
    x = hkdf(4096,root_key,session_key)
    root_key = x[:2048]
    comm_key = x[2048:] #Enfin on a la clé de chiffrement du message 

    # MAJ des keys local pour cette conversation


    #tricks pour faire 2 messages d'affilé, on n'envoie pas de key sur le deuxième message
    eph_pub = "NONE" #on remplace la clé éphemère par un token NONE
    
    keys += str(eph_pub) #on fini de preparer la variable keys qui contiend toute les clés à transférer


    # chiffrement
    # Signature ....
    (x,y)=generate_sign(data,p,q,g,my_id_priv)
    signature=str(x)+":"+str(y) # on concatène les deux parties de la signature 

    # ID
    msg_id = str(random.randint(10000, 100000))
    # date 
    date = str(time.time())
    # stocker le message sur le serveur
    with open(server_msg_path,'a') as f :
        output = "\n"+myID+","+receiver+","+msg_id+","+date+","+data+",MSG,"+keys+","+signature #origin,dest,id,date,data=ACK,type=ACK,keys,signature
        f.write(output)
     # stocker le message en local ATTENTION A mettre le message en clair en local
    with open(personnal_msg,'a') as f:
            output = "\n"+myID+","+receiver+","+ msg_id+","+"False"+","+date+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)

if __name__=="__main__":
    myID = input("Enter your name : ")
    print("Bonjour ",myID," !")


    personnal_msg = "personnal_data/"+myID+".msg"
    personnal_keys = "personnal_data/"+myID+".keys"

    # Nouvel user ?

    # generation et de clés
    # stockage et de clés


    # inititalisation des variables perso
    my_id_priv = 0
    my_id_pub = 0
    
    
    with open(personnal_msg,'a')as f:#création des files
        pass
    with open(personnal_keys,'a')as f:
        pass
    server_key_path = "server.keys"
    server_msg_path = "server.msg"
    while True : 
        check_msg()
        k = input("message ? ")
        if k =="o":
            send_msg()
        k = input("check conv ? ")
        if k =="o":
            a= input("Qui ? : ")
            check_conv(a)
        time.sleep(10)