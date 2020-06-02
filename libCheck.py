from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
import png2


def generateKey(n, e, d):
    keyPair = RSA.construct((n, e, d))
    kluczPubliczny = keyPair.publickey()
    return keyPair, kluczPubliczny


def libCheck(n, e, d):
    keyPair, kluczPubliczny = generateKey(n, e, d)
    msg = 'daasddsfafasddadsddaadsdasdasdsadasdasdadasdadasdasadsdasdasdasdasdas'
    msg = bytes(msg, 'ascii')
    encryptor = PKCS1_OAEP.new(kluczPubliczny)
    encrypted = encryptor.encrypt(msg)

    decryptor = PKCS1_OAEP.new(keyPair)
    decrypted = decryptor.decrypt(encrypted)
    return decrypted == msg


def rsaLibImage(n, e, d, filename1, filename4, filename5):
    # wielkosc dla szyfrowania biblioteka
    blockSize2 = 64
    keyPair, kluczPubliczny = generateKey(n, e, d)
    png2.encryptPNG(filename1, filename4, kluczPubliczny,  blockSize2)
    png2.decryptPNG(filename4, filename5, keyPair)
