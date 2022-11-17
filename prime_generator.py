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
    n=30#3076-512
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
    q = generate_prime(n = 10)
    p = prime_from_prime(q)
#n=3072 prime"""42319497670192821545946615252209673109677225028613892412561386782526930920583767194139955881001195614668775056120404415013148090951892954204953909865916795037269938465835747093967448520123816629302706544939395131405659753939183809402981935857266275419317363356979266075303232855495809448782012453565615220666359358597692203498934195533397118957309475530089462348663140647771188572603816330556171310194843968069269597715463407705438237909279601180783489982448491361578170614483778384033872254117814346539879827151387383182980444307667080622689463771297923414369153073665931997870285588226267462998861424143849380040760062189397904328901233915250848860200442291669324552424156186921362931705560674921077997437286080141422507991846514280479735357586258220163014074338615507450563623709715452897143169784539524624496307339027346522137698586918638418412741868881039059232376594450944027944747638311678179270400393304330239805571567"""
#n=512 corresponding prime"""6987996590433036289133966107502273878194324094372457338088403547531577896701394141824845328358861006000565922233052113753739754313712307851443210692660973"""
#Verified (p-1)%q=0
#Verified (p-1)//q=....