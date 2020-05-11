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


def makeKeyFiles(name, keySize):
    # Creates two files 'x_publickey.txt' and 'x_privatekey.txt'
    # (where x is the value in name) with the the n, e and d, e integers written in them,
    # delimited by a comma.
    if os.path.exists('%s_publickey.txt' % (name)) or os.path.exists('%s_privatekey.txt' % (name)):
        sys.exit('WARNING: The file %s_publickey.txt or %s_privatekey.txt already exists! Use a different name or delete these files and re-run this program.' % (name, name))
    publicKey, privateKey = generateKey(keySize)
    print()
    print('The public key is a %s and a %s digit number.' %
          (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing public key to file %s_publickey.txt...' % (name))

    fo = open('%s_publickey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, publicKey[0], publicKey[1]))
    fo.close()
    print()
    print('The private key is a %s and a %s digit number.' %
          (len(str(publicKey[0])), len(str(publicKey[1]))))
    print('Writing private key to file %s_privatekey.txt...' % (name))

    fo = open('%s_privatekey.txt' % (name), 'w')
    fo.write('%s,%s,%s' % (keySize, privateKey[0], privateKey[1]))
    fo.close()
