from random import randint



BLOC_SIZE = 4096 #taille en bits d'un bloc à chiffrer
BYTESBLOC_SIZE = BLOC_SIZE//8 #taille en byte d'un bloc à chiffrer
ROUNDS = 50

#génération d'une clé de 2048 bits de manière aléatoire


def encodeMessage(message:bytes,key:bytes):

    #bourrage du message
    reste = len(message) % BYTESBLOC_SIZE
    message = message + b'\x00' * (BLOC_SIZE//8 - reste)

    nbBlocs = len(message)//BYTESBLOC_SIZE
    
    cipherMessage=b''

    #chiffrage du message bloc par bloc en utilisant la fonction encodeBloc
    for i in range (nbBlocs):

        subMessage = message[i*BYTESBLOC_SIZE:(i+1)*(BYTESBLOC_SIZE)] #taille BYTESBLOC_SIZE octets
        cipherMessage += int.to_bytes((encodeBloc(int.from_bytes(subMessage, 'little'),key)),BYTESBLOC_SIZE,'little') #encodage d'un bloc de BYTESBLOC_SIZE bytes en int
    return cipherMessage

def decodeMessage(message:bytes,key:bytes):
    
    nbBlocs = len(message)//BYTESBLOC_SIZE

    clearMessage=b''

    #déchiffrage du message chiffré bloc par bloc en utilisant la fonction decodeBloc
    for i in range (nbBlocs):
        
        subMessage = message[i*BYTESBLOC_SIZE:(i+1)*(BYTESBLOC_SIZE)] #taille BYTESBLOC_SIZE octets
        clearMessage += int.to_bytes(decodeBloc(int.from_bytes(subMessage, 'little'),key), BYTESBLOC_SIZE,'little')
    return clearMessage

def encodeBloc(bloc,key): #bloc de type int

    

    #séparation du bloc en parties gauche et droite
    left, right = splitBloc(bloc)

    for i in range(ROUNDS):

        #calcul de la sous-clé
        key = ((key & 0b11) << BLOC_SIZE//2-2 | key >> 2)

        #calcul de r+1 et l+1
        left, right = right, left ^ feistel(right,key)
        
    #concaténation des parties
    bloc = (left << BLOC_SIZE//2 | right)

    return bloc

def decodeBloc(bloc,key):
    
    #séparation du bloc en parties gauche et droite
    left, right = splitBloc(bloc)

    for i in range(ROUNDS):

        #calcul de la sous clé
        key = KEY
        for j in range(ROUNDS - i):
            key = ((key & 0b11) << BLOC_SIZE//2-2 | key >> 2)

        #calcul de r+1 et l+1
        left, right = right ^ feistel(left, key), left
        
    #concaténation des parties    
    bloc = (left << BLOC_SIZE//2 | right)

    return bloc

def splitBloc(bloc):
    left = bloc >> BLOC_SIZE//2
    right = bloc & (2**(BLOC_SIZE//2)-1)
    return left,right

def feistel(bloc, key):
    return bloc ^ key

if __name__=='__main__':  
    message = b'  aaaaaaaaaaaavghrtrtrtrtrtrtrtrt                    htrhtrhtr                '*35
    KEY = randint(2**(BLOC_SIZE//2-1),2**(BLOC_SIZE//2))
    #with open("Memoire.pdf",'rb') as f :
    #    message = f.read()
    print(len(message))
    count = [0]*256
    cipher = encodeMessage(message,KEY)
    print("cipher message:",cipher)
    print("")
    for byte in cipher :
        count[int(byte)]+=1
    mean = 0
    for x in count :
        mean += x
    mean = mean /256
    ecartType = 0
    for x in count :
        ecartType += (x-mean)**2
    ecartType=(ecartType/256)**0.5
    print(ecartType)
    print(count)
    print(decodeMessage(cipher, KEY))
    input()
