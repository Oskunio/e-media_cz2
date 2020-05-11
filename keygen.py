from Crypto.Util import number
import random
import sys
import os


def generateKey(keySize):
    # Step 1: Create two prime numbers, p and q. Calculate n = p * q.
    print('Generating p prime...\n')
    p = number.getPrime(keySize)
    print('Generating q prime...\n')
    q = number.getPrime(keySize)
    n = p * q

    # Step 2: Create a number e that is relatively prime to (p-1)*(q-1).
    print('Generating e that is relatively prime to (p-1)*(q-1)...\n')
    while True:
        e = random.randrange(2 ** (keySize - 1), 2 ** (keySize))
        if number.GCD(e, (p - 1) * (q - 1)) == 1:
            break

    # Step 3: Calculate d, the mod inverse of e.
    print('Calculating d that is mod inverse of e...\n')
    d = number.inverse(e, (p - 1) * (q - 1))
    publicKey = (n, e)
    privateKey = (n, d)
    print('Public key:\n', publicKey, "\n")
    print('Private key:\n', privateKey, "\n")
    return (publicKey, privateKey)
