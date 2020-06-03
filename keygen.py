from Crypto.Util import number
import random
import sys
import os


def getKeyValues(keyLength):
    if not os.path.exists('publickey.txt') and not os.path.exists('privatekey.txt'):
        makeKeyFiles(keyLength)

    # getting n and e from publickey.txt
    with open("publickey.txt", "r") as publickey:
        for line in publickey:
            currentline = line.split(",")
            n = int(currentline[1])
            e = int(currentline[2])

    # getting d from privatekey.txt
    with open("privatekey.txt", "r") as privatekey:
        for line in privatekey:
            currentline = line.split(",")
            d = int(currentline[1])
    return n, e, d


def HexStringToPNG(filename, newFile):
    data = bytes.fromhex(newFile)
    with open(filename, 'wb') as file:
        file.write(data)
    file.close()


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
    privateKey = (d)
    print('Public key:\n', publicKey, "\n")
    print('Private key:\n', privateKey, "\n")
    return (publicKey, privateKey)


def makeKeyFiles(keySize):
    # Creates two files 'publickey.txt' and 'privatekey.txt'
    # with the the n, e and d integers written in them,
    # delimited by a comma.
    publicKey, privateKey = generateKey(keySize)

    fo = open('publickey.txt', 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()

    fo = open('privatekey.txt', 'w')
    fo.write('%s,%s' % (keySize, privateKey))
    fo.close()
    print("Successfully created keys!")
