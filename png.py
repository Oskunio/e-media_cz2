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

def encryptPNG(filename1,filename2, n, e, blockSize):
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
        while i < realLength:
            block = idatHex[i:i+blockSize]
            i = i+blockSize
            encryptedBlock = encryptBlock(block,n,e,blockSize)
            newIDAT += encryptedBlock
        newIdatLength = int(len(newIDAT) / 2)
        print(newIdatLength)
        newIdatLengthHex = format(newIdatLength,'x')
        while len(newIdatLengthHex) % 8 != 0:
            newIdatLengthHex = '0' + newIdatLengthHex
        newFile = hexFile[0:(posInText-8)] + newIdatLengthHex + hexFile[posInText:(posInText+8)]  + newIDAT + hexFile[(posInText+realLength):]
        HexStringToPNG(filename2, newFile)

def encryptBlock(block,n,e,blockSize):

    blockInt= int(block,16)
    encryptedBlock = rsa_algorithm.encrypt(blockInt,n,e)
    hexBlock = format(encryptedBlock,'x')
    leng = len(hexBlock) # 256
    while len(hexBlock) % blockSize != 0:
        hexBlock = '0' + hexBlock
    return hexBlock

def decryptPNG(filename1,filename2, n, e):
    handler = open(filename1, 'rb')
    hexFile = handler.read().hex()
    posInText = hexFile.find("49444154")

    if posInText != -1:
        length = hexFile[(posInText - 8):posInText]
        chunkLengthDec = int(length, 16)
        realLength = 2 * chunkLengthDec
        idatHex = hexFile[(posInText + 8):(posInText + 8 + realLength)]
        newIDAT = ''
        i = 0
        while i < realLength:
            block = idatHex[i:i + 256]
            i = i + 256
            encryptedBlock = decryptBlock(block, n, e)
            newIDAT += encryptedBlock
        newIdatLength = int(len(newIDAT) / 2)
        print(newIdatLength)
        newIdatLengthHex = format(newIdatLength, 'x')
        while len(newIdatLengthHex) % 8 != 0:
            newIdatLengthHex = '0' + newIdatLengthHex
        newFile = hexFile[0:(posInText - 8)] + newIdatLengthHex + hexFile[posInText:(posInText + 8)] + newIDAT + hexFile[(posInText + realLength):]
        HexStringToPNG(filename2, newFile)

def decryptBlock(block,n,e):

    blockInt= int(block,16)
    encryptedBlock = rsa_algorithm.decrypt(blockInt,n,e)
    hexBlock = format(encryptedBlock,'x')
    length = len(hexBlock) #powinno być tyle ile blockSize w encryptPNG czyli 64
    if length % 2 != 0:
        hexBlock = '0' + hexBlock
    return hexBlock















