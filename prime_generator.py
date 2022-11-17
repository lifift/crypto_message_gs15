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
if __name__ == '__main__':
    generate_prime(n = 3072)
"""4292469091081941787852573722304873042379196201997918874258631027848536688666827404638258423522505378195480739223209688942029116059567909798690586120923435711468396310369223166553370616241775320020540836189417921172571346899975021302225524130824045771697337039920702707588891418679721071314241329538864793408023803304160377255979162158488484079098824519353831063189527593195492499997241834018709545739809430344890081174734932033933935709577259601376896266240781383219600530896764205096055830415184011507805552472203518550846432638892160751530988879981470697076071149504769330957847616005805163638772962268223049985774171568506091708263340533607694656704926954043533527881141287595911660122327533214644131363509231003483764735398762066126129411638696127452747414357618935505276153072550980933417734636289988317302378971100378670646443529015947640530148744362674371132014560246827800011978515504461654824551649458834019416213551"""