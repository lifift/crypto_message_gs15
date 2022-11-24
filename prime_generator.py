# SOURCES : https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/

# Large Prime Generation for RSA
import random
 
# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
 
def nBitRandom(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)

def randFromPrime(q):
    n=2048-512
    return (1+q*random.randrange(2**(n-1)+1, 2**n - 1)) #p-1=z*q
 
def getLowLevelPrime(n):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)
 
         # Test divisibility by pre-generated
         # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else: return pc

def getLowLevelPrime2(q):
    '''Generate a prime candidate divisible
    by first primes'''
    while True:
        # Obtain a random number
        pc = randFromPrime(q)
 
         # Test divisibility by pre-generated
         # primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else: return pc
 
def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)
 
    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True
 
    # Set number of trials here
    numberOfRabinTrials = 30
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True
 
def generate_prime(n):
    while True:
        
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            print(n, "bit prime is: \n", prime_candidate)
            return(prime_candidate)

def prime_from_prime(q):
    while True:
        
        prime_candidate = getLowLevelPrime2(q)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            print("bit prime is: \n", prime_candidate)
            return(prime_candidate)


if __name__ == '__main__':
    q = generate_prime(n = 512)
    p = prime_from_prime(q)
#n=2048 prime"""25609898604414818356342675008980494897320973700032729042741978847955470690563539315503075260137954424218767802738997491883941727288933895582915811782129793113275820909132179284450321438003081904632732477602364083710534888696619971023354520651427561951597944508962735793879190401444321968298703993398341618781322304367199429931812771382884008170204285496824709993303257154803236932656743437511594862201976855434608648427127824768146417075316608933153693677113483567374237103917039356104683891533551327116768970260095980834507885270535254322555436964641024641901789777790118207151853051452357282161018449250985923122741"""
#n=512 corresponding prime"""10898621702918512854645648131019767490988342061643920779545576456895643674524554995206186169110085936609320715829241238089007233226152798270438965200688221"""
#Verified (p-1)%q=0 x
#Verified (p-1)//q=....