def rc4(key:bytes, message:bytes):
    #print("key : ",str(key))
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
        output += int.to_bytes(message[x]^K,1,'little')
    return output
    

if __name__== "__main__" :
    key=b'hello'
    message=b'  yooooooooooooooooooooooooooo         '
    count = [0]*256
    result= rc4(key,message)
    print (result)
    for byte in result :
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
    print(rc4(key,result))
