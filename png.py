import keygen
import rsa_algorithm
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random

def HexStringToPNG(filename, newFile):
    data = bytes.fromhex(newFile)
    with open(filename, 'wb') as file:
        file.write(data)
    file.close()

def encryptPNG(filename1,filename2, n, e, keySize):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
    posInText = hexFile.find("49444154")

    if posInText != -1:
        length = hexFile[(posInText - 8):posInText]
        chunkLengthDec = int(length, 16)
        realLength = 2 * chunkLengthDec
        idatHex = hexFile[(posInText+8):(posInText + 8 + realLength)]
        newIDAT = ''
        i = 0
        while i != realLength:
            block = idatHex[i:i+4]
            i = i+4
            encryptedBlock = encryptBlock(block,n,e)
            newIDAT += encryptedBlock
        newIdatLength = int(len(newIDAT) / 2)
        print(newIdatLength)
        newIdatLengthHex = format(newIdatLength,'x')
        while len(newIdatLengthHex) != 8:
            newIdatLengthHex = '0' + newIdatLengthHex
        newFile = hexFile[0:(posInText-8)] + newIdatLengthHex + hexFile[posInText:(posInText+8)]  + newIDAT + hexFile[(posInText+realLength):]
        HexStringToPNG(filename2, newFile)

def encryptBlock(block,n,e):
    #lefBracket = '5b'
    #rightBracket = '5d'
    blockInt= int(block,16)
    encryptedBlock = rsa_algorithm.encrypt(blockInt,n,e)
    hexBlock = format(encryptedBlock,'x')
    length = len(hexBlock)
    if length % 2 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock

















