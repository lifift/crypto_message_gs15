def rc4(key:bytes, message:bytes):
    output=b''
    S=list(range(256))
    T=[]
    j=0
    for i in range (255) :
        j = (j + S[i] + key[i%len(key)] )% 256
        #swap des valeurs 
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
    (i,j) = (0,0)
    genOut=True
    for x in range (len(message)) :
        i = (i+1)%256
        j = (j+S[i])%256
        #swap des valeurs 
        temp = S[i]
        S[i] = S[j]
        S[j] = temp
        K = S[(S[i]+S[j])%256]
        output += int.to_bytes(message[x]^K)
    return output
    

if __name__== "__main__" :
    key=b'hello'
    message=b'je ne mange pas de glace a la vanille'
    result= rc4(key,message)
    print (result)
    print(rc4(key,result))
