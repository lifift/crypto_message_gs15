from random import randint



BLOC_SIZE = 512 #taille en bits d'un bloc à chiffrer
BYTESBLOC_SIZE = BLOC_SIZE//8 #taille en byte d'un bloc à chiffrer
ROUNDS = 50

#fonction d'encodage d'un message
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

#fonction de decodage d'un message
def decodeMessage(message:bytes,key:bytes):
    
    nbBlocs = len(message)//BYTESBLOC_SIZE

    print("nbBlocs : ",nbBlocs)

    clearMessage=b''

    #déchiffrage du message chiffré bloc par bloc en utilisant la fonction decodeBloc
    for i in range (nbBlocs):
        
        subMessage = message[i*BYTESBLOC_SIZE:(i+1)*(BYTESBLOC_SIZE)] #taille BYTESBLOC_SIZE octets
        clearMessage += int.to_bytes(decodeBloc(int.from_bytes(subMessage, 'little'),key), BYTESBLOC_SIZE,'little')
    return clearMessage

#fonction d'encodage d'un bloc
def encodeBloc(bloc,key): #bloc de type int

    #séparation du bloc en parties gauche et droite
    left, right = splitBloc(bloc)

    for i in range(ROUNDS):

        #calcul de la sous-clé
        key = ((key & 0b11) << BLOC_SIZE//2-i | key >> i)

        #calcul de r+1 et l+1
        left, right = right, left ^ feistel(right,key)
        
    #concaténation des parties
    bloc = (left << BLOC_SIZE//2 | right)

    return bloc

#fonction de decodage d'un bloc
def decodeBloc(bloc,key):
    
    #séparation du bloc en parties gauche et droite
    left, right = splitBloc(bloc)

    for i in range(ROUNDS):

        #calcul de la sous clé
        key = KEY
        for j in range(ROUNDS - i):
            key = ((key & 0b11) << BLOC_SIZE//2-j | key >> j)

        #calcul de r+1 et l+1
        left, right = right ^ feistel(left, key), left
        
    #concaténation des parties    
    bloc = (left << BLOC_SIZE//2 | right)

    return bloc

#fonction de séparation de bloc en parties droite et gauche
def splitBloc(bloc):
    left = bloc >> BLOC_SIZE//2
    right = bloc & (2**(BLOC_SIZE//2)-1)
    return left,right


#fonction de permutation de feistel : opérations à appliquer sur le bloc à partir de constantes et de la clé
def feistel(bloc, key):

    #constantes 
    h1 = 24265875238220453645199072305570293410238617325561336148823992597139152267818772292448782652563474764135490138334680744596933885102814780649887717079551796664538731655409245387595348292588045512630720811840230125519970852350213973164845445165776277934850944476129232729496650255108254278943851608284319843401110890825240357642767101161265914081980735205758658041602162484835131055120539275597563576277429641315622982874526175828084317730299656253510357488226084910664253695804840612769048377217205603973520353397041452511020057601030408798313367416209036983833452170241383811111592315806605843204008613063680400021150
    h2 = 20601116062663082615872078122071191329276421692793245428375275310104208811446030796815161058991178262057731327238133601755587999884519236443129897994088835582425600478312497028102005009674523966433369068987748389433349675909660550739647418432763244285407794368585542716980611039997205692394813833007950765160416949164528531154948814153732217526526032666303687434675303246339928277300337137472984039544535118723810245529373708761511879722707105825946011372384081487628412921197619789988063220636115715110523392606484727770236332506037249175522136569448987395056294290759022696297787929866190079239739614176702586769268

    #opération linéaire
    bloc = bloc*(key + h1) + h2

    #opérations binaires
    bloc ^= key
    bloc += key
    
    return bloc%(2**(BLOC_SIZE//2))


if __name__=='__main__': 
    with open('files/Capture.PNG','rb') as f :

        message = f.read()
    KEY = randint(2**(BLOC_SIZE//2-1),2**(BLOC_SIZE//2))
    cipher = encodeMessage(message,KEY)
    with open('files/coded_img.png','ab') as f :
        f.write(cipher)
    print("cipher message:",cipher)
    print("")
    #print(decodeMessage(cipher, KEY))
    with open('files/decoded_img.png','ab') as f :
        f.write(decodeMessage(cipher, KEY))
