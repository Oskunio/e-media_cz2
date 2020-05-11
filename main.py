from keygen import makeKeyFiles
import rsa_algorithm
import test
import os

if __name__ == '__main__':
    print("RSA")
    if not os.path.exists('publickey.txt') and not os.path.exists('privatekey.txt'):
        makeKeyFiles(1024)
