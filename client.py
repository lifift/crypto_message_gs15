
import time
import random

# selecting a user


# On suppose que les clés sont déja manuellement déposé sur le serveur

def check_msg():# met à jour les messages de "ID" en interrogeant le serveur
    with open(server_msg_path,'r') as f : 
        lines = f.readlines()
    new_msg = []
    with open(server_msg_path, "w") as f:
        for line in lines:
            try : 
                if line.strip("\n").split(',')[1] != myID: #format d'une ligne : origin,dest,id,date,data,?type?
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
            msg      = line.split(',')[5] # On stocke le message en clair
        
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

    if msg_type == "INIT":
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
    data   = input("Entrez votre message : ")
    # ratchet
    # chiffrement
    # ID
    msg_id = str(random.randint(10000, 100000))
    # stocker le message sur le serveur
    with open(server_msg_path,'a') as f :
        output = "\n"+myID+","+receiver+","+msg_id+","+"date.date"+","+data+",MSG" #origin,dest,id,date,data=ACK,type=ACK
        f.write(output)
     # stocker le message en local ATTENTION A mettre le message en clair en local
    with open(personnal_msg,'a') as f:
            output = "\n"+myID+","+receiver+","+ msg_id+","+"False"+","+"date.date"+","+data #sender, receiver, id, ack, date, msg 
            f.write(output)

if __name__=="__main__":
    myID = input("Enter your name : ")
    print("Bonjour ",myID," !")
    personnal_msg = "personnal_data/"+myID+".msg"
    personnal_keys = "personnal_data/"+myID+".keys"
    with open(personnal_msg,'a')as f:
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
        time.sleep(10)